import numpy as np
import skimage.data
from skimage.measure import compare_psnr, compare_ssim
import imageio
import pybm3d
import matplotlib.pyplot as plt

original = imageio.imread('../applications/assets/barbara.png')

for algorithm in ['bm3d', 'ksvd']:
    for sigma in [10, 20, 30, 40, 50, 60]:
        denoised = imageio.imread('barbara_%s_denoised_%s.png' % (algorithm, sigma))
        print("%s with %s: PSNR %s, SSIM %s" % (
            algorithm, sigma, compare_psnr(original, denoised), compare_ssim(original, denoised)
        ))

