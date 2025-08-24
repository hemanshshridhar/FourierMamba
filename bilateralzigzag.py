from collections import defaultdict
import numpy as np
class ProgressiveZigZag(object):
    def flip_matrix_inplace(self,matrix):
        n = len(matrix)
        for i in range(n // 2):
            matrix[i], matrix[n - 1 - i] = matrix[n - 1 - i], matrix[i]
        return matrix 

    def findDiagonalOrder(mat):
        m = mat.size(1)   # number of columns
        mat = mat.numpy()
        mat1 = mat[:, :m//2]   # left half
        mat2 = mat[:, m//2:] 
        mat2 = np.flipud(mat2)                 # flip rows (up ↔ down)
        mat1 = np.flipud(mat1.T)   
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
        for k in range(rows1 + cols1 - 2):
            if k%2 ==0:
                r.extend(d1[k][::-1])
            else:
                r.extend(d1[k])
        for k in range(len(mat2) + len(mat2[0])-1):
            if k%2 ==0:
                r.extend(d2[k][::-1])
            else:
                r.extend(d2[k])

        return r                   

mat = [
    [ 1,  2,  3,  4,  5,  6],
    [ 7,  8,  9, 10, 11, 12],
    [13, 14, 15, 16, 17, 18],
    [19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30],
    [31, 32, 33, 34, 35, 36],
    [37, 38, 39, 40, 41, 42]
]
s = ProgressiveZigZag()
result = s.findDiagonalOrder(mat)
print(result)



