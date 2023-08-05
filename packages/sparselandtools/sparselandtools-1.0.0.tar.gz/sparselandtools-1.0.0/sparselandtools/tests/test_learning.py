import unittest

import numpy as np

from sparselandtools.dictionaries import Dictionary
from sparselandtools.learning import ApproximateKSVD
from sparselandtools.pursuits import MatchingPursuit


class TestLearning(unittest.TestCase):

    @staticmethod
    def bmatrix(a):
        """Returns a LaTeX bmatrix

        :a: numpy array
        :returns: LaTeX bmatrix as a string
        """
        if len(a.shape) > 2:
            raise ValueError('bmatrix can at most display two dimensions')
        lines = str(a).replace('[', '').replace(']', '').splitlines()
        rv = [r'\begin{bmatrix}']
        rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
        rv += [r'\end{bmatrix}']
        return '\n'.join(rv)

    def test_basic_ksvd_new(self):
        M = np.array([
            [1, 0, 0, 1 / np.sqrt(2)],
            [0, 1, 0, 1 / np.sqrt(2)],
            [0, 0, 1, 0]
        ])
        D1 = Dictionary(M)
        y1 = [2, 2, 1]
        y2 = [1, 1, 2]
        Y = np.array([y1, y2]).T
        print(D1.matrix)
        K = ApproximateKSVD(dictionary=D1, pursuit=MatchingPursuit, t=1)
        print(D1.matrix)
        D2, alphas = K.fit(Y, 1)
        print(D1.matrix)
        a1 = MatchingPursuit(dictionary=D1, sparsity=1).fit(Y)

        print(D1.matrix)

        print("E1: ", np.linalg.norm(Y - np.matmul(D1.matrix, a1)))
        print("E2: ", np.linalg.norm(Y - np.matmul(D2.matrix, alphas)))

        print(D2.matrix)


if __name__ == '__main__':
    unittest.main()
