"""
This test generates some of the examples I use in my Master's thesis
and on my blog. Many examples are computationally demanding. I ran
them on an AWS Cloud optimized for numerical applications.

The expected duration of execution is around X hours on an optimized machine.
If you exclude all examples that use the KSVD, the examples can be generated
in under 10 minutes.
"""
import os
import unittest

import matplotlib
import numpy as np
import seaborn as sns

from tests.utils import Example

sns.set(style='ticks', palette='dark')
sns.set_context("paper")
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['axes.labelsize'] = 12
matplotlib.rcParams['legend.frameon'] = False
matplotlib.rcParams['legend.fontsize'] = 11
import imageio
import matplotlib.pyplot as plt

from sparselandtools.dictionaries import DCTDictionary, Dictionary
from sparselandtools.pursuits import MatchingPursuit
from sparselandtools.learning import ApproximateKSVD

from sklearn.feature_extraction import image
from sklearn.datasets import make_blobs

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


class TestExamples(unittest.TestCase):

    def teest_mp_example(self):
        E = Example("3.2", "Sine-MP")
        # begin example
        s = np.linspace(0, 2 * np.pi, 256)
        X = np.sin(s)

        # add random white noise, obtain Y
        np.random.seed(1801)
        sigma = 0.25
        Y = np.array([X + sigma * np.random.randn(256)])

        # create DCTDictionary
        D = DCTDictionary(16, 16)

        # statistics
        mses = []
        ncof = []
        T = 350
        width = 0.025

        for t in range(T):
            # fit data and obtain approximation
            MP = MatchingPursuit(dictionary=D, max_iter=256, tol=t * width)
            A = MP.fit(Y.T)
            Y_appr = np.dot(D.matrix, A)
            mses.append(np.linalg.norm(X - Y_appr.T[0]) ** 2)
            ncof.append(np.count_nonzero(A.T[0]))

        # find best values for eps
        m1 = int(np.argmin(mses))
        m2 = int(np.argmin(ncof))

        MP = MatchingPursuit(dictionary=D, max_iter=256, tol=m1 * width)
        A = MP.fit(Y.T)
        Y_appr1 = np.dot(D.matrix, A)

        MP = MatchingPursuit(dictionary=D, max_iter=256, tol=m2 * width)
        A = MP.fit(Y.T)
        Y_appr2 = np.dot(D.matrix, A)

        data = np.array([s, X, Y, [m1, m2], mses, ncof, Y_appr1, Y_appr2, [width, T]])
        np.save(E.path(), data)

    def teest_reconstruction(self):
        barbara = imageio.imread('../applications/assets/barbara.png')
        barbara = barbara.astype('float32')
        patches = image.extract_patches_2d(barbara, (8, 8))

        data = np.load(os.path.join('outputs', '3.3-K-SVD') + '.npy')
        D = Dictionary(data[2])

        Y = np.array([p.reshape(64) for p in patches])
        A = MatchingPursuit(D, sparsity=4).fit(Y.T)

        Yh = np.matmul(D.matrix, A)
        Y_recon = [p.reshape(8, 8) for p in Yh.T]
        Y_recon = image.reconstruct_from_patches_2d(np.array(Y_recon), (512, 512))

        np.save('outputs/recon.npy', Y_recon)

    def teest_woodpecker(self):
        barbara = imageio.imread('../applications/assets/technion.jpg')[:, :, 0]
        barbara = barbara.astype('float32')
        patches = image.extract_patches_2d(barbara, (8, 8))
        print(patches.shape)
        np.random.seed(1801)
        samples = 6200
        idx = np.random.randint(patches.shape[0], size=samples)
        Y = np.array([p.reshape(64) for p in patches[idx]])

        D = DCTDictionary(8, 11)
        K = ApproximateKSVD(D, MatchingPursuit, 4)
        D2, alphas = K.fit(Y.T, 50)

        np.save('outputs/technion.npy', D2.matrix)

        plt.imshow(D2.as_patches(), cmap='gray')
        plt.show()

    def test_k_means(self):
        fs = (3, 3)
        C = np.array([
            [1, 1],
            [0.5, 2.0]
        ])
        centers = np.array([
            [0, 1],
            [1, 2]
        ])
        Y, t = make_blobs(n_samples=20, n_features=2, centers=centers, cluster_std=0.2, random_state=11)
        plt.figure(figsize=fs)
        plt.xticks([])
        plt.yticks([])
        plt.xlim(-0.35, 1.3)
        plt.ylim(0.25, 2.5)
        plt.scatter(Y[:, 0], Y[:, 1], color='#C8C8C8')
        color = ['#332288', '#EE6677']
        for i, c in enumerate(C):
            plt.plot(c[0], c[1], marker='v', color=color[i])
        colors = []
        red = []
        blue = []
        for i, y in enumerate(Y):
            err = [np.linalg.norm(y - c) for c in C]
            if err[0] <= err[1]:
                colors.append(color[0])
                red.append(i)
            else:
                colors.append(color[1])
                blue.append(i)

        plt.savefig("outputs/figures/KM1.pdf", bbox_inches='tight', pad_inches=0)
        plt.figure(figsize=fs)
        plt.xticks([])
        plt.yticks([])
        plt.xlim(-0.35, 1.3)
        plt.ylim(0.25, 2.5)
        for i, c in enumerate(C):
            plt.plot(c[0], c[1], marker='v', color=color[i])
        plt.scatter(Y[:, 0], Y[:, 1], c=colors)
        plt.savefig("outputs/figures/KM2.pdf", bbox_inches='tight', pad_inches=0)

        plt.figure(figsize=fs)
        plt.xticks([])
        plt.yticks([])
        plt.xlim(-0.35, 1.3)
        plt.ylim(0.25, 2.5)
        plt.scatter(Y[:, 0], Y[:, 1], color='#C8C8C8')

        C[0] = 1 / len(red) * sum([Y[i] for i in red])
        C[1] = 1 / len(blue) * sum([Y[i] for i in blue])

        for i, c in enumerate(C):
            plt.plot(c[0], c[1], marker='v', color=color[i])

        plt.savefig("outputs/figures/KM3.pdf", bbox_inches='tight', pad_inches=0)
        plt.figure(figsize=fs)
        plt.xticks([])
        plt.yticks([])
        plt.xlim(-0.35, 1.3)
        plt.ylim(0.25, 2.5)
        colors = []
        red = []
        blue = []
        for i, y in enumerate(Y):
            err = [np.linalg.norm(y - c) for c in C]
            if err[0] <= err[1]:
                colors.append(color[0])
                red.append(i)
            else:
                colors.append(color[1])
                blue.append(i)
        for i, c in enumerate(C):
            plt.plot(c[0], c[1], marker='v', color=color[i])
        plt.scatter(Y[:, 0], Y[:, 1], c=colors)
        plt.savefig("outputs/figures/KM4.pdf", bbox_inches='tight', pad_inches=0)
        plt.show()


if __name__ == '__main__':
    unittest.main()
