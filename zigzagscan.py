import numpy as np

def zigzag_indices(N):
    idxs = []
    for s in range(2*N - 1):
        i_start = max(0, s - (N - 1))
        i_end   = min(N - 1, s)
        diag = [(i, s - i) for i in range(i_start, i_end + 1)]
        if s % 2 == 0:
            diag.reverse()
        idxs.extend(diag)
    return idxs

def zigzag_scan(block):
    N = block.shape[0]
    idxs = zigzag_indices(N)
    return np.array([block[i, j] for (i, j) in idxs])

def zigzag_inverse(seq, N):
    idxs = zigzag_indices(N)
    block = np.zeros((N, N), dtype=seq.dtype)
    for k, (i, j) in enumerate(idxs):
        block[i, j] = seq[k]
    return block


# Example block
dataBlock2D = np.array([
    [1,  2,  3,  4,  5,  6,  7,  8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17,18, 19, 20, 21, 22, 23, 24],
    [25,26, 27, 28, 29, 30, 31, 32],
    [33,34, 35, 36, 37, 38, 39, 40],
    [41,42, 43, 44, 45, 46, 47, 48],
    [49,50, 51, 52, 53, 54, 55, 56],
    [57,58, 59, 60, 61, 62, 63, 64]
])

# Zigzag scan
seq = zigzag_scan(dataBlock2D)
print("Zigzag sequence (first 20 values):")
print(seq[:32])

# Reconstruction
recon = zigzag_inverse(seq, 8)
print("\nReconstruction matches original?", np.allclose(recon, dataBlock2D))



