import unittest
import numpy as np

from dictionaries import Dictionary, DCTDictionary, HaarDictionary, RandomDictionary


class TestDictionaries(unittest.TestCase):

    def test_unitary(self):
        M = np.eye(4)
        D = Dictionary(M)
        self.assertTrue(D.is_unitary())

    def test_normalized(self):
        M = np.array([
            [1, 0, 0, 0, 1/np.sqrt(2)],
            [0, 1, 0, 0, 1/np.sqrt(2)],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0]
        ])
        D = Dictionary(M)
        self.assertTrue(D.is_normalized())

    def test_mutual_coherence(self):
        M = np.array([
            [1, 0, 0, 0, 1 / np.sqrt(2)],
            [0, 1, 0, 0, 1 / np.sqrt(2)],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0]
        ])
        D = Dictionary(M)
        self.assertTrue(np.isclose(D.mutual_coherence(), 1/np.sqrt(2)))

    def test_get_item(self):
        M = np.eye(2)
        D = Dictionary(M)
        self.assertTrue(np.allclose(M[:,1], D[:,1]))

    def test_dct_dictionary(self):
        D = DCTDictionary(16, 16)
        self.assertTrue(D.is_unitary())
        print(D.mutual_coherence())

    def test_haar_dictionary(self):
        D = HaarDictionary(16, 16)
        self.assertTrue(D.is_unitary())

    def test_overcomplete_dct_dictionary(self):
        D = DCTDictionary(8, 21)
        print(D.matrix.shape)

    def test_overcomplete_haar_dictionary(self):
        D = HaarDictionary(8, 21)
        print(D.matrix.shape)

    def test_random_dictionary(self):
        D = RandomDictionary(8, 8)

    def test_visualization(self):
        D = RandomDictionary(8, 8)
        D.as_patches()


class TestTransforms(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()