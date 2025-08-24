from collections import defaultdict
import torch
import numpy as np
class ProgressiveZigZag(object):
    def flip_matrix_inplace(self,matrix):
        n = len(matrix)
        for i in range(n // 2):
            matrix[i], matrix[n - 1 - i] = matrix[n - 1 - i], matrix[i]
        return matrix 
    def _transpose(self,mat):
        if not mat: 
            return []
        rows, cols = len(mat), len(mat[0])
        return [[mat[r][c] for r in range(rows)] for c in range(cols)]
    def mirror(self,A):
        m = len(A)     
        n = len(A[0])     
        B = [[0]*m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                B[i][j] = A[m-1-j][n-1-i]
        return B

    def findDiagonalOrder(mat):
        m = mat.size(1)   # number of columns
        mat = mat.numpy()
        mat1 = mat[:, :m//2]   # left half
        mat2 = mat[:, m//2:] 
        mat2 = np.flipud(mat2)                 # flip rows (up ↔ down)
        mat1 = np.flipud(mat1.T)               # transpose, then flip rows
        
        d1 = defaultdict(list)
        d2 = defaultdict(list)
        
        
        rows2, cols2 = mat2.size()
        for i in range(rows2):
            for j in range(cols2):
                d2[i+j].append(mat2[i,j].item())
        rows1, cols1 = mat1.shape
        for i in range(rows1):
            for j in range(cols1):
                d1[i+j].append(mat1[i,j].item())

        r = []
        
        r.extend(d1[0])
        N = rows1 + cols2 - 2
        i,j = 1 ,0
        while i <= N or j <= N:
            for _ in range(2):
                if j <= N:
                    if j%2==0:
                        r.extend(d2[j][::-1])
                        
                    else:
                        r.extend(d2[j])                        
                    j +=1
            for _ in range(2):
                if i <= N:
                    if i%2==0:
                        r.extend(d1[i][::-1])
                    else:
                        r.extend(d1[i])
                    i +=1
        return r                   

mat = [
[1, 2, 3, 4, 5, 6, 7, 8],
[9, 10, 11, 12, 13, 14, 15, 16],
[17, 18, 19, 20, 21, 22, 23, 24],
[25, 26, 27, 28, 29, 30, 31, 32],
[33, 34, 35, 36, 37, 38, 39, 40],
[41, 42, 43, 44, 45, 46, 47, 48],
[49, 50, 51, 52, 53, 54, 55, 56]
]
s = ProgressiveZigZag()
result = s.findDiagonalOrder(mat)
print(result)


