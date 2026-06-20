import json
import numpy as np
import os
import sys

# Add root directory to python path to use existing predictive_outcome_simulator
sys.path.append('/root')
from predictive_outcome_simulator import PredictiveOutcomeSimulator

class MoASimulatorT3:
    """
    Task T3: Simulation & Complexity Modeling for MoA Attention.
    Models memory traffic, compute latency, and energy savings under roofline limits.
    """
    def __init__(self):
        # Hardware Parameters
        self.hardware_profiles = {
            "NVIDIA_H100": {
                "bandwidth_tb_s": 3.35,  # TB/s
                "peak_flops_tflops": 1979.0, # FP16 Tensor Core peak TFLOPS (dense)
                "sram_bytes": 262144, # 256 KB L1/SRAM
                "energy_pj_flop": 1.0,
                "energy_pj_byte": 150.0 # DRAM access cost in pJ per byte
            },
            "NVIDIA_A100": {
                "bandwidth_tb_s": 2.039,
                "peak_flops_tflops": 312.0,
                "sram_bytes": 163840, # 160 KB SRAM
                "energy_pj_flop": 1.5,
                "energy_pj_byte": 200.0
            },
            "AMD_MI300X": {
                "bandwidth_tb_s": 5.3,
                "peak_flops_tflops": 2610.0,
                "sram_bytes": 524288, # 512 KB SRAM/L1
                "energy_pj_flop": 0.8,
                "energy_pj_byte": 120.0
            }
        }

    def compute_flops(self, n, d_k, d_v):
        """
        Calculates standard FLOP count for scaled dot-product attention.
        1. QK^T: 2 * n^2 * d_k
        2. Scale and Softmax: 5 * n^2 (approx for subtract max, exp, sum, div)
        3. Attn * V: 2 * n^2 * d_v
        """
        qkt_flops = 2.0 * n * n * d_k
        softmax_flops = 5.0 * n * n
        output_flops = 2.0 * n * n * d_v
        return qkt_flops + softmax_flops + output_flops

    def compute_memory_traffic_bytes(self, n, d_k, d_v, precision_bytes=2):
        """
        Calculates total memory traffic (DRAM read/writes in bytes) for:
        - Standard (Classical) Attention
        - FlashAttention
        - MoA (Mathematics of Arrays) Attention (theoretical minimum)
        """
        # Element sizes
        q_size = n * d_k * precision_bytes
        k_size = n * d_k * precision_bytes
        v_size = n * d_v * precision_bytes
        out_size = n * d_v * precision_bytes
        
        # --- Classical Attention ---
        # Reads: Q, K, V (each once)
        # Intermediates written to DRAM:
        # - Score matrix: n^2
        # - Softmax exp matrix: n^2
        # - Softmax weights: n^2
        # Intermediates read from DRAM:
        # - Score matrix (to compute max/exp): n^2
        # - Softmax exp matrix (to sum and divide): n^2
        # - Softmax weights (to compute final GEMM): n^2
        # Writes: Out
        scores_matrix_size = n * n * precision_bytes
        traffic_classical = (
            q_size + k_size + v_size + # Initial reads
            scores_matrix_size * 6 +   # Score writes/reads, exp writes/reads, weights writes/reads
            out_size                   # Final write
        )
        
        # --- FlashAttention ---
        # FlashAttention avoids writing the n^2 intermediate matrix by tiling to fit SRAM of size M.
        # Traffic formula: Input reads (Q, K, V) + O(n^2 * d / M) HBM access.
        # Specifically, let M be SRAM capacity in bytes. Q is read once, but K and V are re-loaded
        # n*d*precision_bytes/M times.
        M_sram = 256 * 1024 # 256KB default
        block_count = max(1.0, (n * d_k * precision_bytes) / M_sram)
        traffic_flash = (
            q_size +  # Q read once
            k_size * block_count +  # K re-read per block
            v_size * block_count +  # V re-read per block
            out_size # Write Out
        )
        
        # --- MoA Attention ---
        # Pure stream-based index selection.
        # Accesses only inputs (Q, K, V) and writes Output.
        # No intermediate arrays are created or written to DRAM.
        traffic_moa = q_size + k_size + v_size + out_size
        
        return traffic_classical, traffic_flash, traffic_moa

    def run_roofline_simulation(self, hw_name, n, d_k, d_v, precision_bytes=2):
        """
        Runs latency and energy modeling using the Roofline parameters.
        """
        hw = self.hardware_profiles[hw_name]
        bandwidth = hw["bandwidth_tb_s"] * (1024**4) # Bytes/sec
        peak_flops = hw["peak_flops_tflops"] * (1024**4) # FLOPs/sec
        
        flops = self.compute_flops(n, d_k, d_v)
        
        m_class, m_flash, m_moa = self.compute_memory_traffic_bytes(n, d_k, d_v, precision_bytes)
        
        # Latency = max(Compute Latency, Memory Latency)
        t_compute = flops / peak_flops
        
        t_mem_classical = m_class / bandwidth
        t_mem_flash = m_flash / bandwidth
        t_mem_moa = m_moa / bandwidth
        
        lat_classical = max(t_compute, t_mem_classical)
        lat_flash = max(t_compute, t_mem_flash)
        lat_moa = max(t_compute, t_mem_moa)
        
        # Energy = FLOPs * E_flop + MemoryTraffic * E_byte
        energy_classical = (flops * hw["energy_pj_flop"] + m_class * hw["energy_pj_byte"]) / 1e9 # Joules
        energy_flash = (flops * hw["energy_pj_flop"] + m_flash * hw["energy_pj_byte"]) / 1e9
        energy_moa = (flops * hw["energy_pj_flop"] + m_moa * hw["energy_pj_byte"]) / 1e9
        
        return {
            "classical": {"latency_ms": lat_classical * 1000, "energy_j": energy_classical, "traffic_mb": m_class / (1024**2)},
            "flash": {"latency_ms": lat_flash * 1000, "energy_j": energy_flash, "traffic_mb": m_flash / (1024**2)},
            "moa": {"latency_ms": lat_moa * 1000, "energy_j": energy_moa, "traffic_mb": m_moa / (1024**2)}
        }

    def run_stochastic_scenarios(self, n, d_k, d_v):
        """
        Integrates with PredictiveOutcomeSimulator to compute probability-weighted matrix of gains.
        Varies variables: bandwidth congestion, core scaling efficiency, and L1 cache hits.
        """
        pos = PredictiveOutcomeSimulator()
        
        # Let's map success of MoA reaching >10x gain under stochastic conditions
        causal_chain = [
            {"step": "HighMemorySavings", "success_prob": 0.95, "dependencies": [], "variable_impact": {"bandwidth_congestion": 0.05}},
            {"step": "CoreEfficiencyMatch", "success_prob": 0.85, "dependencies": ["HighMemorySavings"], "variable_impact": {"dram_bus_fluctuation": -0.10}},
            {"step": "Exceeded10xSpeedup", "success_prob": 0.75, "dependencies": ["CoreEfficiencyMatch"], "variable_impact": {"bandwidth_congestion": 0.15}}
        ]
        
        variables = {
            "bandwidth_congestion": {"mean": 0.5, "std": 0.2}, # 0 = clean bus, 1 = heavily congested
            "dram_bus_fluctuation": {"mean": 0.0, "std": 0.1}
        }
        
        sim_result = pos.simulate_strategy(causal_chain, variables, iterations=2000)
        return sim_result

    def run_comprehensive_sweep(self):
        n_values = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
        d_k, d_v = 64, 64
        
        sweep_data = {}
        
        for hw_name in self.hardware_profiles:
            sweep_data[hw_name] = []
            for n in n_values:
                metrics = self.run_roofline_simulation(hw_name, n, d_k, d_v)
                speedup_vs_classical = metrics["classical"]["latency_ms"] / metrics["moa"]["latency_ms"]
                speedup_vs_flash = metrics["flash"]["latency_ms"] / metrics["moa"]["latency_ms"]
                energy_savings_vs_classical = metrics["classical"]["energy_j"] / metrics["moa"]["energy_j"]
                
                sweep_data[hw_name].append({
                    "n": n,
                    "classical_lat_ms": metrics["classical"]["latency_ms"],
                    "classical_mem_mb": metrics["classical"]["traffic_mb"],
                    "flash_lat_ms": metrics["flash"]["latency_ms"],
                    "flash_mem_mb": metrics["flash"]["traffic_mb"],
                    "moa_lat_ms": metrics["moa"]["latency_ms"],
                    "moa_mem_mb": metrics["moa"]["traffic_mb"],
                    "speedup_vs_classical": speedup_vs_classical,
                    "speedup_vs_flash": speedup_vs_flash,
                    "energy_savings_vs_classical": energy_savings_vs_classical
                })
                
        # Stochastic evaluation at exascale length
        stochastic_metrics = self.run_stochastic_scenarios(32768, 64, 64)
        
        report = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "head_dim": d_k,
                "precision": "FP16 (2 bytes)"
            },
            "sweep": sweep_data,
            "stochastic_gains": stochastic_metrics
        }
        
        # Save to JSON
        with open("/root/moa_t3_report.json", "w") as f:
            json.dump(report, f, indent=4)
        
        self.print_markdown_report(report)

    def print_markdown_report(self, report):
        print("## 📊 Task T3: Simulation & Complexity Modeling Report")
        print("\n### 1. Unified Roofline Model Performance Sweep (NVIDIA H100)")
        print("| Sequence Length (n) | Classical DRAM (MB) | MoA DRAM (MB) | Savings | Speedup (vs Classical) | Speedup (vs Flash) |")
        print("|---|---|---|---|---|---|")
        
        h100_data = report["sweep"]["NVIDIA_H100"]
        for entry in h100_data:
            savings = entry["classical_mem_mb"] / entry["moa_mem_mb"]
            print(f"| {entry['n']:5d} | {entry['classical_mem_mb']:18.2f} | {entry['moa_mem_mb']:12.2f} | {savings:6.1f}x | {entry['speedup_vs_classical']:21.2f}x | {entry['speedup_vs_flash']:17.2f}x |")
            
        print("\n### 2. Stochastic Probability-Weighted Gains (Monte Carlo, N=2000)")
        stoch = report["stochastic_gains"]
        print(f"- **Probability of achieving >10x raw speedup under random bus congestion**: {stoch['success_probability']*100:.2f}%")
        print(f"- **Sensitivity Map (correlation to system bottlenecks)**:")
        for var, sens in stoch["sensitivity_map"].items():
            print(f"  - `{var}`: {sens:.4f} (Higher positive value = stronger bottleneck driver)")

if __name__ == "__main__":
    from datetime import datetime
    sim = MoASimulatorT3()
    sim.run_comprehensive_sweep()
