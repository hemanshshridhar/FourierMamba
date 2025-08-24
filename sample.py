import torch
import numpy as np
from collections import defaultdict
import numpy as np
from collections import defaultdict
import torch
def findDiagonalOrder(mat,flip =False):
    m = mat.size(1)   # number of columns in torch tensor
    mat = mat.numpy()
    mat1 = mat[:, :m//2]   # left half
    mat2 = mat[:, m//2:] 
    mat2 = np.flipud(mat2)                 # flip rows (up ↔ down)
    mat1 = np.flipud(mat1.T)               # transpose, then flip rows
    
    d1, d2 = defaultdict(list), defaultdict(list)
    
    rows2, cols2 = mat2.shape   # ✅ use .shape in NumPy
    for i in range(rows2):
        for j in range(cols2):
            d2[i+j].append(mat2[i, j])
    
    rows1, cols1 = mat1.shape
    for i in range(rows1):
        for j in range(cols1):
            d1[i+j].append(mat1[i, j])

    r = []
    r.extend(d1[0])
    N = rows1 + cols2 - 2
    i, j = 1, 0
    while i <= N or j <= N:
        for _ in range(2):
            if j <= N:
                if j % 2 == 0:
                    r.extend(d2[j][::-1])
                else:
                    r.extend(d2[j])
                j += 1
        for _ in range(2):
            if i <= N:
                if i % 2 == 0:
                    r.extend(d1[i][::-1])
                else:
                    r.extend(d1[i])
                i += 1
    rd = np.array(r)
    if flip == True:
        rd = np.flip(rd)
    # 🔑 Convert Python list → NumPy array
    return rd




def findDiagonalOrder(mat):
    # if torch tensor, make it numpy safely
    if isinstance(mat, torch.Tensor):
        mat = mat.detach().cpu().numpy()

    m = mat.shape[1]             # number of columns (NumPy)
    mat1 = mat[:, :m//2]         # left half
    mat2 = mat[:, m//2:]         # right half
    mat2 = np.flipud(mat2)       # flip rows (up ↔ down)
    mat1 = np.flipud(mat1.T)     # transpose, then flip rows

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

    # consume all diagonals of mat1
    for k in range(rows1 + cols1 - 1):            # FIX: -1, not -2
        r.extend(d1[k][::-1] if k % 2 == 0 else d1[k])

    # then all diagonals of mat2
    for k in range(rows2 + cols2 - 1):
        r.extend(d2[k][::-1] if k % 2 == 0 else d2[k])

    return np.array(r)             # return as NumPy array
mat = torch.arange(1, 17).reshape(4, 4)  # 4x4 tensor
out = findDiagonalOrder(mat)
print(type(out))  # <class 'numpy.ndarray'>
print(out.shape)  # (16,)
print(out)