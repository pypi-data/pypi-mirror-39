import os
import random

import numpy as np

"""
    Discrete Hopfield Network (DHNN) implemented with Python.
"""


class DHNN(object):

    def __init__(self, isload=False, wpath='weigh.npy'):

        self.wpath = wpath
        if isload and os.path.isfile(wpath):
            print("Loading weight matrix....")
            self.weight = np.load(wpath)
        else:
            self.weight = None

    def update(self, y, theta=0.5, epochs=100):
        """Update test sample.

        Arguments:
            y {np.ndarray} -- vector

        Keyword Arguments:
            theta {float} -- the threshold of the neuron activation(default: {0.5})
            epochs {int} -- the max iteration of loop(default: {100})

        Returns:
            np.ndarray -- recoveried sample
        """

        length = len(y)
        for _ in range(epochs):
            ind = random.randint(0, length-1)
            u = np.dot(self.weight[ind], y) - theta
            if u > 0:
                y[ind] = 1
            elif u < 0:
                y[ind] = -1

        return y

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

    def train(self, data, save=True):
        """Training pipeline.

        Arguments:
            data {list} -- each sample is vector

        Keyword Arguments:
            save {bool} -- save weight or not (default: {True})
        """

        if self.weight is None:
            print("Creating weight matrix....")
            self.weight = self.create_W(data)
            print("Weight matrix is done!")

            if save:
                np.save(self.wpath, self.weight)

    def predict(self, data, epochs=1000, theta=0.5):
        """Predicting pipline.

        Arguments:
            data {list} -- each sample is vector

        Keyword Arguments:
            epochs {int} -- the max iteration of loop (default: {1000})
            theta {float} -- the threshold of the neuron activation (default: {0.5})

        Returns:
            list -- recoveried by hopfield data 
        """

        recovery = []
        for counter, y in enumerate(data):
            print("The {}th sample is updating...".format(counter))
            recovery.append(self.update(y=y, theta=theta, epochs=epochs))

        return recovery
