import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings
class PCA():
    def __init__(self):
        self.data = None
        self.dimension = 1
        self.decline = None
        self.value = None
    def input(self,data,dimension):
        if data.shape[0] != dimension:
            raise Exception("Check your data's dimension,they didn't fit.")
        else:
            self.data = data
            mean = np.array([np.mean(self.data,axis=1)]).T
            self.data = self.data - np.tile(mean,(1,data.shape[1]))
    def set_dimension(self,x):
        if x < 1 or int(x) != x:
            raise Exception("Dimension can't be this:(Int and larger than 0)", x)
        else:
            self.dimension = x
    def Decline(self):
        cov = np.cov(self.data)
        self.value, vector = np.linalg.eig(cov)
        self.decline = vector[0:self.dimension].dot(self.data)
        return self.decline
    def check(self,plot=False):
        if plot == True:
            plt.plot(self.value)
            plt.show()
        return np.sum(self.value)


if __name__ == '__main__':
    data = np.array([[-1, -2, 1, 5],
                     [-1, 0, 3, 6],
                     [0, 0, 5, 7.5],
                     [2, 1, 6, 8],
                     [0, 1, 8, 10]
                     ]).T
    pca = PCA()
    pca.input(data,4)
    pca.set_dimension(3)
    result = pca.Decline()
    pca.check(plot=True)


