import json
import math

n_values = [1024, 8192, 32768, 65536]
h = 32
d_k = 128
d_v = 128
b = 1
bytes_per_param = 2 # FP16
vram_constraint_bytes = 32 * 1024**3 # 32 GB

# Base memory model overhead (weights + fixed buffers) -> 14 GB
base_model_mem = 14 * 1024**3

results = []

for n in n_values:
    # O(n^2) Traditional Attention Intermediate Memory: b * h * n * n
    trad_attention_matrix_mem = b * h * n * n * bytes_per_param
    # Base KV cache: 2 (K,V) * b * h * n * d * 2 bytes
    kv_cache_mem = 2 * b * h * n * d_k * bytes_per_param
    
    total_trad_mem = base_model_mem + kv_cache_mem + trad_attention_matrix_mem
    
    # O(nd) MoA Attention Intermediate Memory: b * h * n * (d_k + d_v)
    moa_intermediate_mem = b * h * n * (d_k + d_v) * bytes_per_param
    total_moa_mem = base_model_mem + kv_cache_mem + moa_intermediate_mem
    
    reduction_pct = ((trad_attention_matrix_mem - moa_intermediate_mem) / trad_attention_matrix_mem) * 100
    
    # Calculate OOM Prob: Step sigmoid around constraint
    def calc_oom_prob(mem):
        diff_gb = (mem - vram_constraint_bytes) / (1024**3)
        if diff_gb < -2: return 0.0
        elif diff_gb > 2: return 1.0
        else: return 1.0 / (1.0 + math.exp(-diff_gb * 2))

    trad_oom_prob = calc_oom_prob(total_trad_mem)
    moa_oom_prob = calc_oom_prob(total_moa_mem)
    
    # Silent pivot multiplier (inversely proportional to trad success, directly to moa success)
    trad_success = 1.0 - trad_oom_prob
    moa_success = 1.0 - moa_oom_prob
    silent_pivot = (moa_success + 0.01) / (trad_success + 0.01)

    results.append({
        "n": n,
        "n_squared_intermediate_GB": trad_attention_matrix_mem / (1024**3),
        "nd_intermediate_GB": moa_intermediate_mem / (1024**3),
        "trad_total_GB": total_trad_mem / (1024**3),
        "moa_total_GB": total_moa_mem / (1024**3),
        "reduction_pct": reduction_pct,
        "trad_oom_prob": trad_oom_prob,
        "moa_oom_prob": moa_oom_prob,
        "silent_pivot_multiplier": silent_pivot
    })

print(json.dumps(results, indent=2))
