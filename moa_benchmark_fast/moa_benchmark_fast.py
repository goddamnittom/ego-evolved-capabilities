import numpy as np
import time

def standard_attention(Q, K, V):
    d_k = Q.shape[-1]
    scores = np.matmul(Q, K.T) / np.sqrt(d_k)
    max_scores = np.max(scores, axis=-1, keepdims=True)
    exp_scores = np.exp(scores - max_scores)
    sum_exp = np.sum(exp_scores, axis=-1, keepdims=True)
    attn_weights = exp_scores / sum_exp
    output = np.matmul(attn_weights, V)
    return output

def moa_vectorized_row_attention(Q, K, V):
    n, d_k = Q.shape
    _, d_v = V.shape
    sqrt_dk = np.sqrt(d_k)
    Output = np.zeros((n, d_v), dtype=np.float64)
    for i in range(n):
        scores_i = np.dot(K, Q[i]) / sqrt_dk
        max_i = np.max(scores_i)
        exp_i = np.exp(scores_i - max_i)
        denom_i = np.sum(exp_i)
        y_i = exp_i / denom_i
        Output[i] = np.dot(y_i, V)
    return Output

def moa_blocked_attention(Q, K, V, block_size=256):
    n, d_k = Q.shape
    _, d_v = V.shape
    sqrt_dk = np.sqrt(d_k)
    Output = np.zeros((n, d_v), dtype=np.float64)
    for i in range(0, n, block_size):
        end = min(i + block_size, n)
        Q_block = Q[i:end]
        scores_block = np.matmul(Q_block, K.T) / sqrt_dk
        max_block = np.max(scores_block, axis=-1, keepdims=True)
        exp_block = np.exp(scores_block - max_block)
        denom_block = np.sum(exp_block, axis=-1, keepdims=True)
        y_block = exp_block / denom_block
        Output[i:end] = np.matmul(y_block, V)
    return Output

if __name__ == "__main__":
    np.random.seed(42)
    n_values = [500, 1000, 2000]
    d_k, d_v = 64, 64
    
    print("--- Running Fast MoA Attention Benchmark ---")
    for n in n_values:
        print(f"\n--- Sequence Length (n={n}) ---")
        Q = np.random.randn(n, d_k)
        K = np.random.randn(n, d_k)
        V = np.random.randn(n, d_v)
        
        # Standard
        t0 = time.time()
        out_std = standard_attention(Q, K, V)
        t_std = time.time() - t0
        print(f"Standard Attention:      {t_std:8.4f}s | Memory: {n*n*8 / (1024*1024):6.2f} MB")
        
        # Row-by-Row
        t0 = time.time()
        out_row = moa_vectorized_row_attention(Q, K, V)
        t_row = time.time() - t0
        print(f"Row-by-Row MoA Attention: {t_row:8.4f}s | Memory: {n*8 / 1024:6.2f} KB | Diff: {np.max(np.abs(out_std - out_row)):.2e}")
        
        # Blocked (B=128)
        t0 = time.time()
        out_blk_128 = moa_blocked_attention(Q, K, V, block_size=128)
        t_blk_128 = time.time() - t0
        print(f"Blocked MoA (B=128):     {t_blk_128:8.4f}s | Memory: {128*n*8 / (1024*1024):6.2f} MB | Diff: {np.max(np.abs(out_std - out_blk_128)):.2e}")

        # Blocked (B=256)
        t0 = time.time()
        out_blk_256 = moa_blocked_attention(Q, K, V, block_size=256)
        t_blk_256 = time.time() - t0
        print(f"Blocked MoA (B=256):     {t_blk_256:8.4f}s | Memory: {256*n*8 / (1024*1024):6.2f} MB | Diff: {np.max(np.abs(out_std - out_blk_256)):.2e}")
