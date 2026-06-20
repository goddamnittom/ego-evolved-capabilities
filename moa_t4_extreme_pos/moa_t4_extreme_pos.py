import numpy as np
import json
from dataclasses import dataclass

@dataclass
class PosMetrics:
    flops: int
    memory_traffic_bytes: int
    l1_cache_hit_rate: float
    arithmetic_intensity: float
    max_skew_diff: float
    oom_prob: float
    simulated_latency_ms: float

def moa_dnf_stable_softmax_block_test(B, d_k, skew):
    """
    Validates MoA DNF stability under Softmax Extreme Skew constraints.
    Injects high variance/skew to trigger standard overflow, testing DNF max-shift stabilization.
    """
    Q = np.random.randn(B, d_k).astype(np.float64) * skew
    K = np.random.randn(B, d_k).astype(np.float64)
    V = np.random.randn(B, d_k).astype(np.float64)
    
    scale = 1.0 / np.sqrt(d_k)
    S = (Q @ K.T) * scale
    
    # Causal mask (constraint check)
    mask = np.triu(np.ones((B, B)), k=1).astype(bool)
    S[mask] = -np.inf
    
    # DNF MoA Online Max-Shifting
    row_max = np.max(S, axis=1, keepdims=True)
    row_max[row_max == -np.inf] = 0 
    
    S_shifted = S - row_max
    exp_S = np.exp(S_shifted)
    exp_S[mask] = 0.0
    
    sum_exp_S = np.sum(exp_S, axis=1, keepdims=True)
    A = exp_S / (sum_exp_S + 1e-9)
    
    # Return numerical stability delta (should be stable, no NaNs)
    has_nan = np.isnan(A).any()
    max_val = np.max(A) if not has_nan else float('inf')
    return float(max_val), has_nan

def moa_causal_bma_simulate(N, d_k, d_v, B, dtype='fp16', skew_factor=100.0):
    bytes_per_elem = 2 if dtype == 'fp16' else 1
    
    # 1. Softmax Extreme Skew check
    max_val, has_nan = moa_dnf_stable_softmax_block_test(B, d_k, skew_factor)
    
    # 2. Roofline I/O Tracking (Causal)
    num_blocks = N // B
    total_flops = 0
    total_hbm_bytes = 0
    
    # Causal structure: num passes = N*(N+1)/2 blocks
    total_kv_blocks = (num_blocks * (num_blocks + 1)) // 2
    
    # Every Q block is loaded from HBM
    total_hbm_bytes += num_blocks * B * d_k * bytes_per_elem
    # Every matched KV block is loaded
    total_hbm_bytes += total_kv_blocks * (B * d_k + B * d_v) * bytes_per_elem
    # Output blocks stored
    total_hbm_bytes += num_blocks * B * d_v * bytes_per_elem
    
    # FLOPs constraint
    # QK^T: 2 * B^2 * d_k per KV block
    total_flops += total_kv_blocks * 2 * B * B * d_k
    # Score * V: 2 * B^2 * d_v per KV block
    total_flops += total_kv_blocks * 2 * B * B * d_v
    
    # 3. L1 Cache Simulation
    l1_size = 32 * 1024 # 32 KB
    # Working set: 1 Q block + 1 K block + 1 V block + 1 O block
    working_set_bytes = B * (d_k * 2 + d_v * 2) * bytes_per_elem
    l1_hit_rate = 0.95 if working_set_bytes <= l1_size else (l1_size / working_set_bytes) * 0.5
    
    arithmetic_intensity = total_flops / total_hbm_bytes
    
    # Predict Latency assuming realistic ~300 TFLOPs and typical memory bandwidth bottlenecks
    theoretical_tflops_ms = total_flops / 312e9 
    hbm_bandwidth_gb_ms = 1.5e6 # 1.5 TB/s = 1500 GB/s = 1.5e6 bytes/ms
    theoretical_hbm_ms = total_hbm_bytes / hbm_bandwidth_gb_ms
    
    latency_ms = max(theoretical_tflops_ms, theoretical_hbm_ms)
    
    # Memory footprint validation against N=65536 extreme condition
    # Requires only blocks + output, not N^2
    actual_memory_req = (N * d_v + working_set_bytes) 
    oom_prob = 0.0 if actual_memory_req < 80 * 1024**3 else 1.0 # 80GB VRAM cap
    
    return PosMetrics(
        flops=total_flops,
        memory_traffic_bytes=total_hbm_bytes,
        l1_cache_hit_rate=float(l1_hit_rate),
        arithmetic_intensity=float(arithmetic_intensity),
        max_skew_diff=max_val,
        oom_prob=oom_prob,
        simulated_latency_ms=float(latency_ms)
    )

if __name__ == "__main__":
    print("Executing Phase T4 POS Models (Constraints Active)...")
    results = {}
    
    # Baseline Scenario 1: FP16, Standard high scale
    N_test = 65536
    # FP16, B=128 fits aggressively in L1
    metrics_fp16 = moa_causal_bma_simulate(N_test, d_k=256, d_v=256, B=64, dtype='fp16', skew_factor=1000.0)
    results['MoA_FP16_B64_Causal'] = metrics_fp16.__dict__
    
    # Scenario 2: High d_k (512), INT8
    metrics_int8 = moa_causal_bma_simulate(N_test, d_k=512, d_v=512, B=128, dtype='int8', skew_factor=5000.0)
    results['MoA_INT8_HighDK_Causal'] = metrics_int8.__dict__
    
    # Scenario 3: L1 Cash Thrash Model (B=1024 overrides L1)
    metrics_fp16_thrash = moa_causal_bma_simulate(N_test, d_k=256, d_v=256, B=1024, dtype='fp16', skew_factor=50.0)
    results['MoA_FP16_L1_Thrash_B1024'] = metrics_fp16_thrash.__dict__

    print(json.dumps(results, indent=2))

