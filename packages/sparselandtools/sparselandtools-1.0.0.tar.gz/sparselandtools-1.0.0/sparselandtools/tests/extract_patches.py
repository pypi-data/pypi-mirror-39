import imageio
import matplotlib.pyplot as plt
import numpy as np

from tests.test_learning import TestLearning

img = imageio.imread('../applications/assets/barbara.png')
img = img.astype('float32') / 255
(N, M) = img.shape
n = 2 * 2
ns = int(np.sqrt(n))
img = img.reshape((N * N, 1))

x = 2
y = 3

R = np.zeros((n, N * N))

"""
This worked for x=y=1:
for k in range(0, ns):
    for l in range(0, ns):
        R[l+k*ns, l + k*N] = 1
"""

for k in range(0, ns):
    for l in range(0, ns):
        R[l + k * ns, (y - 1) + (x - 1) * N + l + k * N] = 1

p = np.matmul(R, img)

plt.imshow(p.reshape((ns, ns)), cmap='gray')

Y = np.array([1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16])
print(Y.shape)
N = 4
R = np.zeros((n, N * N))
for k in range(0, ns):
    for l in range(0, ns):
        R[l + k * ns, (x - 1) + (y - 1) * N + l + k * N] = 1
print(R)
print(np.matmul(R, Y))

R = np.array(R, dtype=int)
print(TestLearning.bmatrix(R))

plt.show()
