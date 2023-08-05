import os
import numpy as np
import seaborn as sns
import imageio
import matplotlib
sns.set(style='ticks', palette='hls')
sns.set_context("paper")
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['axes.labelsize'] = 12
matplotlib.rcParams['legend.frameon'] = False
matplotlib.rcParams['legend.fontsize'] = 11
import matplotlib.pyplot as plt
from dictionaries import Dictionary, DCTDictionary
from tests.psnr import psnr
from sklearn.feature_extraction import image
from skimage import measure


def generate_plot(specifier):

    if specifier == "cartoon":
        data = np.load(os.path.join('outputs', specifier) + '.npy')
        D = Dictionary(data)
        fig, ax = plt.subplots(figsize=plt.figaspect(D.as_patches()))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(D.as_patches(), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'output.pdf')

    if specifier == "woodpecker":
        data = np.load(os.path.join('outputs', specifier) + '.npy')
        D = Dictionary(data)
        fig, ax = plt.subplots(figsize=plt.figaspect(D.as_patches()))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(D.as_patches(), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'output.pdf')

    if specifier == "technion":
        data = np.load(os.path.join('outputs', specifier) + '.npy')
        D = Dictionary(data)
        fig, ax = plt.subplots(figsize=plt.figaspect(D.as_patches()))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(D.as_patches(), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'output.pdf')

    if specifier == "recon":
        data = np.load(os.path.join('outputs', specifier) + '.npy')
        barbara = imageio.imread('../applications/assets/barbara.png')
        barbara = barbara.astype('float32')

        fig, ax = plt.subplots(figsize=plt.figaspect(data))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(data, cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'BARB.pdf')
        plt.show()

        fig, ax = plt.subplots(figsize=plt.figaspect(data))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(np.abs(barbara-data), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'DIFF.pdf')
        plt.show()

        print("PSNR: ", measure.compare_psnr(barbara, data, data_range=255))
        print("SSIM: ", measure.compare_ssim(barbara, data))
        print("MSE: ", measure.compare_mse(barbara, data))

    if specifier == "3.2-Sine-MP":
        data = np.load(os.path.join('outputs', specifier) + '.npy')
        s = data[0]
        X = data[1]
        Y = data[2]
        m1 = data[3][0]
        m2 = data[3][1]
        mses = data[4]
        ncof = data[5]
        Y_appr1 = data[6]
        Y_appr2 = data[7]
        width = data[8][0]
        T = data[8][1]
        plt.figure(figsize=(12,5))
        plt.subplot(2,2,1)
        plt.plot(s, Y[0], color='#d0d0d0', label='noisy')
        plt.plot(s, X, color='#000000', label='original')
        plt.legend()
        plt.subplot(2,2,2)
        plt.plot(s, Y[0], color='#d0d0d0')
        plt.plot(s, Y_appr1.T[0], color='r')
        plt.plot(s, Y_appr2.T[0], color='b')
        plt.subplot(2, 2, 3)
        plt.ylabel('number of non-zeros in $a$')
        plt.xlabel(r'$\varepsilon$')
        plt.plot(np.arange(T) * width, ncof, color='#000000')
        plt.plot(m1 * width, ncof[m1], 'ro', label=r'$( \varepsilon=%s, \|| \alpha \||_0=%s)$' % (m1 * width, ncof[m1]))
        plt.plot(m2 * width, ncof[m2], 'bo', label=r'$( \varepsilon=%s, \|| \alpha \||_0=%s)$' % (m2 * width, ncof[m2]))
        plt.legend()
        plt.subplot(2, 2, 4)
        plt.ylabel('Mean Squared Error')
        plt.xlabel(r'$\varepsilon$')
        plt.plot(np.arange(T) * width, mses, color='#000000')
        plt.plot(m1 * width, mses[m1], 'ro')
        plt.plot(m2 * width, mses[m2], 'bo')
        plt.savefig('outputs/figures/' + specifier + 'plot.pdf', bbox_inches='tight', transparent=True, pad_inches=0)
        plt.show()

    elif specifier == "3.3-K-SVD":
        # range(1, iter), err, D2, alphas
        data = np.load(os.path.join('outputs', specifier) + '.npy')
        data2 = np.load(os.path.join('outputs', '3.5-K-SVD') + '.npy')
        data3 = np.load(os.path.join('outputs', '3.4-K-SVD') + '.npy')
        plt.figure(figsize=(6,3))
        plt.plot(data[0], 255/25500*np.array(data[1]), label='Approximate K-SVD DCT-II', color='k')
        plt.plot(data[0], 255/25500*np.array(data2[1]), label='Approximate K-SVD Haar', color='k', linestyle=':')
        #plt.plot(data[0], 255 / 25500 * np.array(data3[1]), label='K-SVD DCT-II', color='k', linestyle='-.')
        plt.ylabel("Average Representation Error")
        plt.xlim(xmin=1)
        plt.legend()
        plt.savefig('outputs/figures/' + specifier + 'ARE.pdf', bbox_inches='tight', transparent=True, pad_inches=0)
        plt.show()
        fig, ax = plt.subplots(figsize=plt.figaspect(DCTDictionary(8, 8).as_patches()))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(Dictionary(data[2]).as_patches(), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'DICT.pdf')
        plt.show()
        fig, ax = plt.subplots(figsize=plt.figaspect(DCTDictionary(8, 8).as_patches()))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(Dictionary(data2[2]).as_patches(), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'DICTHAAR.pdf')
        plt.show()
        fig, ax = plt.subplots(figsize=plt.figaspect(DCTDictionary(8,8).as_patches()))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(DCTDictionary(8,8).as_patches(), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'ORIG_DICT.pdf')
        plt.show()
        fig, ax = plt.subplots(figsize=plt.figaspect(DCTDictionary(8, 8).as_patches()))
        fig.add_axes([0, 0, 1, 1])
        plt.imshow(Dictionary(data3[2]).as_patches(), cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'KSVDREALDICT.pdf')
        plt.show()
        plt.figure()
        plt.axis('off')
        barbara = imageio.imread('../applications/assets/barbara.png')
        barbara = barbara.astype('float32') / 255
        plt.imshow(barbara, cmap='gray')
        plt.savefig('outputs/figures/' + specifier + 'Barbara.pdf', bbox_inches='tight', transparent=True,
                    pad_inches=0)
        plt.show()

        samples=22500
        barbara = imageio.imread('../applications/assets/barbara.png')
        barbara = barbara.astype('float32') / 255
        patches = image.extract_patches_2d(barbara, (8, 8))
        idx = np.random.randint(patches.shape[0], size=samples)
        Y = np.array([p.reshape(64) for p in patches[idx]])

        print("ARE DCT", np.linalg.norm(Y.T - np.matmul(data[2], data[3])))
        print("ARE HAAR", np.linalg.norm(Y.T - np.matmul(data2[2], data2[3])))


if __name__ == '__main__':
    files = os.listdir('outputs')
    files.remove('figures')
    for f in files:
        specifier = f.split('.npy')
        generate_plot(specifier[0])