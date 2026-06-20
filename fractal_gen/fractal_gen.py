import numpy as np

def generate_fractal(fractal_type='mandelbrot', width=500, height=500, max_iter=50, zoom=1, center=(0, 0), c_julia=(-0.7, 0.27015)):
    x_min, x_max = center[0] - 1.5 / zoom, center[0] + 1.5 / zoom
    y_min, y_max = center[1] - 1.5 / zoom, center[1] + 1.5 / zoom
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    if fractal_type == 'julia':
        Z = C
        C = complex(c_julia[0], c_julia[1])
    else:
        Z = np.zeros_like(C)
    fractal = np.full(C.shape, max_iter, dtype=int)
    mask = np.full(C.shape, True, dtype=bool)
    for i in range(max_iter):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        mask[np.abs(Z) > 2] = False
        fractal[mask] = i
    return fractal

mandel = generate_fractal()
# Convert to PGM (Portable Gray Map) - a simple text-based image format
# P2 \n width height \n max_val \n data...
with open('fractal.pgm', 'w') as f:
    f.write(f"P2\n{mandel.shape[1]} {mandel.shape[0]}\n{mandel.max()}\n")
    for row in mandel:
        f.write(" ".join(map(str, row)) + "\n")

print("Fractal generated as PGM file.")
