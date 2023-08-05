import unittest

import numpy as np

from sparselandtools.dictionaries import Dictionary
from sparselandtools.pursuits import MatchingPursuit


class TestPursuits(unittest.TestCase):

    def test_matching_pursuit1d(self):
        M = np.array([
            [1, 0, 0, 0, 1 / np.sqrt(2)],
            [0, 1, 0, 0, 1 / np.sqrt(2)],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0]
        ])
        D = Dictionary(M)
        MP = MatchingPursuit(dictionary=D, sparsity=2)
        Y = np.array([[2.0, 2.0, 0, 1.0]])
        A = MP.fit(Y.T)
        self.assertTrue(np.allclose(np.dot(D.matrix, A), Y.T))


if __name__ == '__main__':
    unittest.main()
