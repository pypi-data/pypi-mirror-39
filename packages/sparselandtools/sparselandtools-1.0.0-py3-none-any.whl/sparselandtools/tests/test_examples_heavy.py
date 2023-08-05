"""
This test generates some of the examples I use in my Master's thesis
and on my blog. Many examples are computationally demanding. I ran
them on an AWS Cloud optimized for numerical applications.

The expected duration of execution is around X hours on an optimized machine.
If you exclude all examples that use the KSVD, the examples can be generated
in under 10 minutes.
"""

import unittest

import matplotlib
import numpy as np

# generate plots, do not display
matplotlib.use('Agg')

import imageio

from sparselandtools.dictionaries import DCTDictionary
from sparselandtools.pursuits import MatchingPursuit
from sparselandtools.learning import ApproximateKSVD
from tests.utils import Example
from sklearn.feature_extraction import image

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'


class TestExamples(unittest.TestCase):

    def test_ksdv(self):
        # define example
        E = Example("3.3", "K-SVD")
        t0 = 4
        iter = 20
        samples = 100
        np.random.seed(1801)
        D = DCTDictionary(8, 8)
        err = []
        barbara = imageio.imread('../applications/assets/barbara.png')
        barbara = barbara.astype('float32') / 255
        patches = image.extract_patches_2d(barbara, (8, 8))
        idx = np.random.randint(patches.shape[0], size=samples)
        Y = np.array([p.reshape(64) for p in patches[idx]])
        for i in range(1, iter):
            print("Iteration: ", i)
            K = ApproximateKSVD(dictionary=D, pursuit=MatchingPursuit, t=t0)
            D2, alphas = K.fit(Y.T, i)
            err.append(np.linalg.norm(Y.T - np.matmul(D2.matrix, alphas)))

        # plt.plot(range(1, iter), err)
        # plt.savefig(E1.output_file(), bbox_inches='tight', transparent=True, pad_inches=0)

        K = ApproximateKSVD(dictionary=D, pursuit=MatchingPursuit, t=t0)
        Y = np.array([p.reshape(64) for p in patches[idx]])
        D2, alphas = K.fit(Y.T, iter)

        # plt.imshow(D2.as_patches(), cmap='gray')
        # plt.savefig(E2.output_file(), bbox_inches='tight', transparent=True, pad_inches=0)
        # plt.show()

        data = np.array([range(1, iter), err, D2.matrix, alphas])
        np.save(E.path(), data)


if __name__ == '__main__':
    unittest.main()
