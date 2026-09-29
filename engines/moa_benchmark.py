import numpy as np
import time

def standard_attention(Q, K, V):
    """
    Standard scaled dot-product attention in NumPy.
    Materializes O(n^2) intermediate arrays in memory.
    """
    d_k = Q.shape[-1]
    scores = np.matmul(Q, K.T) / np.sqrt(d_k)
    max_scores = np.max(scores, axis=-1, keepdims=True)
    exp_scores = np.exp(scores - max_scores)
    sum_exp = np.sum(exp_scores, axis=-1, keepdims=True)
    attn_weights = exp_scores / sum_exp
    output = np.matmul(attn_weights, V)
    return output

def moa_vectorized_row_attention(Q, K, V):
    """
    Vectorized MoA Row-by-Row Attention.
    Operates row-by-row on Q, thereby avoiding the O(n^2) intermediate matrices.
    Instead, it only allocates O(n) memory during the active row computation.
    Leverages high-speed BLAS under the hood via NumPy.
    """
    n, d_k = Q.shape
    _, d_v = V.shape
    sqrt_dk = np.sqrt(d_k)
    
    # Pre-allocate output buffer
    Output = np.zeros((n, d_v), dtype=np.float64)
    
    # Process row-by-row to eliminate O(n^2) memory footprint
    for i in range(n):
        # 1. Compute row-wise scores: shape (1, n)
        # Q[i] is of shape (d_k,), K is of shape (n, d_k).
        # We compute the dot product of Q[i] with all rows of K.
        scores_i = np.dot(K, Q[i]) / sqrt_dk
        
        # 2. Row max for stable softmax
        max_i = np.max(scores_i)
        
        # 3. Exponents and denominator sum
        exp_i = np.exp(scores_i - max_i)
        denom_i = np.sum(exp_i)
        
        # 4. Attention weight row: shape (1, n)
        y_i = exp_i / denom_i
        
        # 5. Output row: shape (d_v,)
        Output[i] = np.dot(y_i, V)
        
    return Output

if __name__ == "__main__":
    # Let's verify correctness on some random inputs
    np.random.seed(42)
    n, d_k, d_v = 1000, 64, 64
    Q = np.random.randn(n, d_k)
    K = np.random.randn(n, d_k)
    V = np.random.randn(n, d_v)
    
    # Correctness check
    print("Verifying correctness of vectorized MoA row-by-row attention...")
    out_std = standard_attention(Q, K, V)
    out_moa = moa_vectorized_row_attention(Q, K, V)
    
    difference = np.max(np.abs(out_std - out_moa))
    print(f"Max absolute difference between Standard and MoA-vectorized: {difference:.2e}")
    assert np.allclose(out_std, out_moa, rtol=1e-12, atol=1e-12), "Outputs do not match!"
    print("✅ CORRECTNESS TEST PASSED!")
    
    # Let's benchmark scalability
    print("\nScaling Benchmarks (n=5000):")
    n = 5000
    Q_large = np.random.randn(n, d_k)
    K_large = np.random.randn(n, d_k)
    V_large = np.random.randn(n, d_v)
    
    # Standard attention benchmark
    t0 = time.time()
    out_std_large = standard_attention(Q_large, K_large, V_large)
    t_std = time.time() - t0
    print(f"Standard Attention time: {t_std:.4f} seconds")
    
    # Vectorized MoA attention benchmark
    t0 = time.time()
    out_moa_large = moa_vectorized_row_attention(Q_large, K_large, V_large)
    t_moa = time.time() - t0
    print(f"Vectorized MoA Row-by-Row Attention time: {t_moa:.4f} seconds")
    
    speed_ratio = t_std / t_moa
    print(f"Speedup ratio: {speed_ratio:.2f}x")
    
    # We should note memory footprint:
    # Standard attention creates standard O(n^2) array of size 5000 * 5000 * 8 bytes = 200 MB
    # Vectorized MoA row attention allocates max O(n) array of size 5000 * 8 bytes = 40 KB
    print(f"Memory allocated for attention score matrix:")
    print(f"  Standard Attention score matrix: {5000*5000*8 / (1024*1024):.2f} MB")
    print(f"  Vectorized MoA Row-by-Row score array: {5000*8 / 1024:.2f} KB")

def moa_blocked_attention(Q, K, V, block_size=256):
    """
    Blocked MoA Attention.
    Processes Q in blocks of size B, reducing the intermediate score matrix
    size from O(n^2) to O(B * n). This balances memory footprint and execution
    speed in Python by avoiding interpreter loop overhead.
    """
    n, d_k = Q.shape
    _, d_v = V.shape
    sqrt_dk = np.sqrt(d_k)
    
    # Pre-allocate output buffer
    Output = np.zeros((n, d_v), dtype=np.float64)
    
    for i in range(0, n, block_size):
        end = min(i + block_size, n)
        Q_block = Q[i:end] # (B, d_k)
        
        # 1. Compute score block: (B, n)
        scores_block = np.matmul(Q_block, K.T) / sqrt_dk
        
        # 2. Block max: (B, 1)
        max_block = np.max(scores_block, axis=-1, keepdims=True)
        
        # 3. Stable exponents: (B, n)
        exp_block = np.exp(scores_block - max_block)
        
        # 4. Denominator sums: (B, 1)
        denom_block = np.sum(exp_block, axis=-1, keepdims=True)
        
        # 5. Attention weights: (B, n)
        y_block = exp_block / denom_block
        
        # 6. Weighted sum for block: (B, d_v)
        Output[i:end] = np.matmul(y_block, V)
        
    return Output

# Append to main benchmark run
if __name__ == "__main__":
    # Correctness check for blocked
    print("\nVerifying correctness of blocked MoA attention...")
    out_blocked = moa_blocked_attention(Q, K, V, block_size=256)
    difference_blocked = np.max(np.abs(out_std - out_blocked))
    print(f"Max absolute difference between Standard and MoA-blocked: {difference_blocked:.2e}")
    assert np.allclose(out_std, out_blocked, rtol=1e-12, atol=1e-12), "Blocked outputs do not match!"
    print("✅ CORRECTNESS TEST FOR BLOCKED PASSED!")
    
    # Large scale benchmark for blocked
    t0 = time.time()
    out_blocked_large = moa_blocked_attention(Q_large, K_large, V_large, block_size=256)
    t_blocked = time.time() - t0
    print(f"Blocked MoA Attention time (block_size=256): {t_blocked:.4f} seconds")
    print(f"Blocked MoA speedup over standard attention: {t_std / t_blocked:.2f}x")
    print(f"Blocked MoA memory footprint: {256*5000*8 / (1024*1024):.2f} MB")

# Let's perform a sweep of block sizes to find the absolute sweet spot
if __name__ == "__main__":
    print("\n--- Sweeping Block Sizes (n=5000) ---")
    block_sizes = [64, 128, 256, 512, 1024, 2048]
    for b in block_sizes:
        t0 = time.time()
        out_b = moa_blocked_attention(Q_large, K_large, V_large, block_size=b)
        t_b = time.time() - t0
        mem_b = b * 5000 * 8 / (1024 * 1024)
        print(f"Block size: {b:4d} | Time: {t_b:.4f}s | Speedup: {t_std / t_b:.2f}x | Memory: {mem_b:6.2f} MB")
