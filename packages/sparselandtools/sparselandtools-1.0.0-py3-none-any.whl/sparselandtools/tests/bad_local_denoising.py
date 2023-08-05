import numpy as np
import skimage.data
from skimage.measure import compare_psnr, compare_ssim
import imageio
import pybm3d
import matplotlib.pyplot as plt

img = imageio.imread('../applications/assets/barbara.png')
img = img.astype('float32')

noise_std_dev = 60
noise = np.random.normal(scale=noise_std_dev,
                         size=img.shape).astype(img.dtype)

img = img.astype('float32') / 255
noise = noise.astype('float32') / 255

noisy_img = img + noise

imageio.imsave('barbara_noisy_%s.png' % noise_std_dev, noisy_img)

plt.imshow(noisy_img)
plt.show()
out = pybm3d.bm3d.bm3d(noisy_img, noise_std_dev/255)
imageio.imsave('barbara_bm3d_denoised_%s.png' % noise_std_dev, out)

noise_psnr = compare_psnr(img, noisy_img)
out_psnr = compare_psnr(img, out)
noise_ssim = compare_ssim(img, noisy_img)
out_ssim = compare_ssim(img, out)

plt.imshow(out)
plt.show()

plt.imshow(noisy_img)


print("PSNR of noisy image: ", noise_psnr)
print("PSNR of reconstructed image: ", out_psnr)
print("SSIM of noisy image: ", noise_ssim)
print("SSIM of reconstructed image: ", out_ssim)