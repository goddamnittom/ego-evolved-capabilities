import numpy as np

def standard_attention_memory(n, d_k, d_v):
    """Memory for Q, K, V (n x d), intermediate scores (n x n), softmax (n x n), Output (n x d)"""
    # Assuming float32 (4 bytes per element)
    input_mem = (n * d_k + n * d_k + n * d_v) * 4
    intermediate_mem = (n * n + n * n) * 4 # Score matrix + Softmax probabilities
    output_mem = (n * d_v) * 4
    return input_mem, intermediate_mem, output_mem

def moa_dnf_attention_memory(n, d_k, d_v):
    """Memory for Q, K, V (n x d), and scalar/vector intermediaries, avoiding n x n."""
    # Input is the same
    input_mem = (n * d_k + n * d_k + n * d_v) * 4
    
    # MoA theoretically reduces the n x n to O(n * d_k). We model it as needing only O(d_k) or O(n) temporary vectors.
    intermediate_mem = (n * d_k + n * d_k) * 4 # Approximating the scalar/vector sweeps
    output_mem = (n * d_v) * 4
    return input_mem, intermediate_mem, output_mem

def run_simulation(n_list, d_k=64, d_v=64):
    print("--- MoA DNF Memory Complexity Simulation ---")
    print(f"Constants: d_k={d_k}, d_v={d_v}, dtype=float32 (4 bytes)")
    print("-" * 75)
    print(f"{'Sequence Length (n)':<20} | {'Classic Memory (GB)':<25} | {'MoA Memory (GB)':<25}")
    print("-" * 75)
    
    results = {}
    
    for n in n_list:
        c_in, c_mid, c_out = standard_attention_memory(n, d_k, d_v)
        m_in, m_mid, m_out = moa_dnf_attention_memory(n, d_k, d_v)
        
        c_total_gb = (c_in + c_mid + c_out) / (1024**3)
        m_total_gb = (m_in + m_mid + m_out) / (1024**3)
        
        ratio = m_total_gb / c_total_gb
        reduction = (1 - ratio) * 100
        
        results[n] = {
            "classic_gb": c_total_gb,
            "moa_gb": m_total_gb,
            "ratio": ratio,
            "reduction_pct": reduction
        }
        print(f"{n:<20} | {c_total_gb:<25.6f} | {m_total_gb:<25.6f}")
        
    print("-" * 75)
    print("Probability-Weighted Memory Gain Map")
    for n, data in results.items():
        print(f"n={n}: MoA requires {data['ratio']:.5f}x the memory of Classic Attention ({data['reduction_pct']:.2f}% reduction)")

if __name__ == '__main__':
    run_simulation([1024, 4096, 8192, 16384, 32768, 65536, 131072])
