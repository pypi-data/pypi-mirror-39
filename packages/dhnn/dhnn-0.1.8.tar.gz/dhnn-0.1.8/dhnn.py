import os

import numba as nb
import numpy as np

__version__ = '0.1.8'

"""
    Discrete Hopfield Network (DHNN) implemented with Python.
"""


# TODO:
# 1. more flag, add 0/1 flag or other flag.
# 1. optimize loop, try numba, Cpython or any other ways.
# 1. optimize memory.


class DHNN(object):

    @nb.autojit
    def __init__(self, isload=False, wpath='weigh.npy'):
        """Initializes DHNN.

        Keyword Arguments:
            isload {bool} -- is load local weight (default: {False})
            wpath {str} -- the local weight path (default: {'weigh.npy'})
        """

        self.wpath = wpath
        if isload and os.path.isfile(wpath):
            self.weight = np.load(wpath)
        else:
            self.weight = None

    @nb.autojit
    def create_W(self, data):
        """Create network weight.

        Arguments:
            data {list} -- each sample is vector.

        Returns:
            np.ndarray -- matrix
        """

        mat = np.vstack(data)
        eye = len(data) * np.identity(np.size(mat, 1))
        weight = np.dot(mat.T, mat) - eye

        return weight

    @nb.autojit
    def train(self, data, issave=False):
        """Training pipeline.

        Arguments:
            data {list} -- each sample is vector

        Keyword Arguments:
            issave {bool} -- save weight or not (default: {True})
        """

        if self.weight is None:
            self.weight = self.create_W(data)

            if issave:
                np.save(self.wpath, self.weight)

    @nb.autojit
    def predict(self, data, theta=0.5, epochs=1000):
        """predict test sample.

        Arguments:
            data {np.ndarray} -- vector

        Keyword Arguments:
            theta {float} -- the threshold of the neuron activation(default: {0.5})
            epochs {int} -- the max iteration of loop(default: {1000})

        Returns:
            np.ndarray -- recoveried sample
        """

        indexs = np.random.randint(0, len(data)-1, epochs)
        for ind in indexs:
            data[ind] = 1 if np.dot(self.weight[ind], data) - theta > 0 else -1

        return data
