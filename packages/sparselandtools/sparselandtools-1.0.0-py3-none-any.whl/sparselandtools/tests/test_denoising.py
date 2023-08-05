import unittest
import imageio

import numpy as np
from sparselandtools.dictionaries import Dictionary, DCTDictionary, HaarDictionary, RandomDictionary
from sparselandtools.pursuits import MatchingPursuit, OrthogonalMatchingPursuit
from sparselandtools.applications.denoising import KSVDImageDenoiser
import matplotlib.pyplot as plt

# load Barbara image
barbara = imageio.imread('../applications/assets/barbara.png')
barbara = barbara.astype('float32')

# make it noisy
noise_std_dev = 20
noise = np.random.normal(scale=noise_std_dev,
                         size=barbara.shape).astype(barbara.dtype)
noisy_img = barbara + noise
plt.imshow(noisy_img, cmap='gray')
plt.show()
patch_size = 8

D = DCTDictionary(8, 8)
print(D.shape)

Denoiser = KSVDImageDenoiser(D, pursuit=OrthogonalMatchingPursuit)

z, d, a = Denoiser.denoise(noisy_img, sigma=20, patch_size=patch_size, n_iter=1, multiplier=0.5, noise_gain=np.sqrt(1.15))
np.save('outputs/z.npy', z)
plt.imshow(z, cmap='gray')
plt.savefig('outputs/figures/' + 'z.pdf')
plt.show()

