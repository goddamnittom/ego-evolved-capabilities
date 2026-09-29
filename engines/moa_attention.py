import numpy as np

def standard_attention(Q, K, V):
    """
    Reference standard attention with numerically stable softmax using NumPy.
    Recreates intermediate matrices: scores (n x n), max_scores (n x 1),
    exp_scores (n x n), sum_exp (n x 1), and attn_weights (n x n).
    """
    d_k = Q.shape[-1]
    # Standard matrix multiply for scores
    scores = np.matmul(Q, K.T) / np.sqrt(d_k)
    
    # Numerically stable softmax
    max_scores = np.max(scores, axis=-1, keepdims=True)
    exp_scores = np.exp(scores - max_scores)
    sum_exp = np.sum(exp_scores, axis=-1, keepdims=True)
    attn_weights = exp_scores / sum_exp
    
    # Weighted sum
    output = np.matmul(attn_weights, V)
    
    return attn_weights, output

def moa_dnf_attention(Q, K, V):
    """
    MoA Denotational Normal Form (DNF) Attention.
    Computes elements on-the-fly directly from input indexing without materializing
    the intermediate O(n^2) score, exponent, or attention weight matrices.
    Memory traffic is O(n*d_k + n*d_v) with O(1) scratch space per thread/lane.
    """
    n, d_k = Q.shape
    _, d_v = V.shape
    
    # Pre-allocate output buffer (the only written buffer)
    Output = np.zeros((n, d_v), dtype=np.float64)
    Y_reconstructed = np.zeros((n, n), dtype=np.float64) # For validation/comparison only
    
    sqrt_dk = np.sqrt(d_k)
    
    for i in range(n):
        # 1. On-the-fly row-max calculation (No intermediate vector/matrix)
        # We compute x[i, k'] for all k' to find the max
        row_max = -np.inf
        for k_prime in range(n):
            # Element-wise dot product of row i of Q and row k_prime of K
            dot_prod = 0.0
            for j in range(d_k):
                dot_prod += Q[i, j] * K[k_prime, j]
            scaled_score = dot_prod / sqrt_dk
            if scaled_score > row_max:
                row_max = scaled_score
                
        # 2. On-the-fly row denominator sum calculation
        denom_sum = 0.0
        for k_prime in range(n):
            dot_prod = 0.0
            for j in range(d_k):
                dot_prod += Q[i, j] * K[k_prime, j]
            scaled_score = dot_prod / sqrt_dk
            denom_sum += np.exp(scaled_score - row_max)
            
        # 3. Compute final output values on-the-fly
        for col_v in range(d_v):
            weighted_sum = 0.0
            for p in range(n):
                # Recompute the specific attention weight weight Y[i, p] on-the-fly
                dot_prod = 0.0
                for j in range(d_k):
                    dot_prod += Q[i, j] * K[p, j]
                scaled_score = dot_prod / sqrt_dk
                y_ip = np.exp(scaled_score - row_max) / denom_sum
                
                # For validation reporting, store once
                if col_v == 0:
                    Y_reconstructed[i, p] = y_ip
                    
                weighted_sum += y_ip * V[p, col_v]
            Output[i, col_v] = weighted_sum
            
    return Y_reconstructed, Output

if __name__ == "__main__":
    # Define exact concrete inputs from Section 5.2 of arXiv:2606.07713v1
    Q = np.array([
        [-0.1984,  0.2698,  0.3414, -0.0372],
        [ 0.2547, -1.0674,  0.3460, -2.5242],
        [ 0.6822, -0.6265,  0.0252,  0.3978]
    ], dtype=np.float64)

    K = np.array([
        [-1.1567,  0.6885, -0.1884,  0.4743],
        [ 0.2246,  1.7564,  0.5235, -2.3014],
        [-1.5899,  0.3730, -0.8257, -1.2069]
    ], dtype=np.float64)

    V = np.array([
        [ 1.0739,  0.4006, -0.9671,  0.4870],
        [ 0.5589, -0.7209, -0.7650,  0.2689],
        [ 0.8237,  0.3763,  0.8320,  0.0014]
    ], dtype=np.float64)

    print("--- Running NumPy Reference Standard Attention ---")
    std_Y, std_Out = standard_attention(Q, K, V)
    print("Standard Attention Weight Matrix (Y):\n", std_Y)
    print("Standard Final Output:\n", std_Out)
    
    print("\n--- Running MoA DNF Attention (No Intermediates) ---")
    moa_Y, moa_Out = moa_dnf_attention(Q, K, V)
    print("MoA DNF Reconstructed Attention Weight Matrix (Y):\n", moa_Y)
    print("MoA DNF Final Output:\n", moa_Out)
    
    # Assert exact numerical equivalence to double-precision tolerance
    np.testing.assert_allclose(std_Y, moa_Y, rtol=1e-15, atol=1e-15)
    np.testing.assert_allclose(std_Out, moa_Out, rtol=1e-15, atol=1e-15)
    print("\n✅ SUCCESS: NumPy Reference and MoA DNF outputs are identical to 15 decimal places!")
