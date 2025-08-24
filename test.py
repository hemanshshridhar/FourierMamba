import torch
import numpy as np

# --- your scan ---
def findDiagonalOrder(mat):
    if isinstance(mat, torch.Tensor):
        mat = mat.detach().cpu().numpy()
    from collections import defaultdict
    m = mat.shape[1]
    mat1 = mat[:, :m//2]
    mat2 = mat[:, m//2:]
    mat2 = np.flipud(mat2)
    mat1 = np.flipud(mat1.T)
    print(mat1)
    print(mat2) 
    d1, d2 = defaultdict(list), defaultdict(list)
    rows2, cols2 = mat2.shape
    for i in range(rows2):
        for j in range(cols2):
            d2[i + j].append(mat2[i, j])
    rows1, cols1 = mat1.shape
    for i in range(rows1):
        for j in range(cols1):
            d1[i + j].append(mat1[i, j])

    r = []
    for k in range(rows1 + cols1 - 1):
        r.extend(d1[k][::-1] if k % 2 == 0 else d1[k])
    for k in range(rows2 + cols2 - 1):
        r.extend(d2[k][::-1] if k % 2 == 0 else d2[k])
    return np.array(r)

def invert_scan_torch(seq_1d, shape_hw, forward_scan_fn, *args, **kwargs):
    """
    seq_1d: 1D torch.Tensor produced by forward_scan_fn(mat)
    shape_hw: (H, W)
    forward_scan_fn can accept numpy arrays or torch tensors; we’ll feed numpy.
    """
    H, W = shape_hw
    # Build numpy index grid and get order via the scan (works even if scan expects torch; convert if needed)
    grid = np.arange(H*W).reshape(H, W)
    order = forward_scan_fn(grid, *args, **kwargs)
    order = np.asarray(order).ravel()
    if order.size != H*W:
        raise ValueError("Scan function did not return H*W elements.")

    seq_1d = seq_1d.reshape(-1)
    if seq_1d.numel() != H*W:
        raise ValueError("Sequence length does not match H*W.")

    out = torch.empty(H*W, dtype=seq_1d.dtype, device=seq_1d.device)
    # Scatter using the order mapping
    out[torch.tensor(order, device=seq_1d.device, dtype=torch.long)] = seq_1d
    return out.view(H, W)
# --- demo on data ---
A = torch.arange(1, 17).reshape(4, 4)
seq = torch.tensor(findDiagonalOrder(A))     # forward scan result (length 16)

# invert (NumPy)
print("Original:\n", A)
print(seq)
# invert (PyTorch)
A_rec_torch = invert_scan_torch(seq, A.shape, findDiagonalOrder)
print("Torch reconstructed:\n", A_rec_torch)

# Verify correctness
print("Matches original? (torch):", torch.equal(A_rec_torch.cpu(), A))