import numpy as np
import warnings
from matplotlib import pyplot as plt
class linear_regression():
    def __init__(self):
        self.data = None
        self.label = None
        self.weight = []
        self.b = 0
        self.number = 0
    def input(self,data,label,init_weight = 0):
        self.data = np.array(data)
        try:
            print("Data's number:"+str(self.data.shape[0]))
            print("Data's dimension:"+str(self.data.shape[1]))
            self.number = self.data.shape[0]
        except:
            raise Exception("Check your data！")
        for i in range(self.data.shape[1]):
            self.weight.append(init_weight)
        self.weight = np.array(self.weight)
        self.b = init_weight
        self.label = np.array(label)
        try:
            print(self.label.shape[1])
            raise Exception("Check your label.Must has 1 dimension and len(label) must equals data's number！")
        except:
            if self.label.shape[0] != self.data.shape[0]:
                raise Exception("Check your label.Must has 1 dimension and len(label) must equals data's number！")
    def fit(self,rang,lr):
        print(self.weight)
        print(self.data)
        print(label)
        print((self.data[1].dot(self.weight)+self.b-self.label[1])*self.data[1])

        for i in range(rang):
            error = self.data[i%self.number].dot(self.weight)+self.b-self.label[i%self.number]
            self.weight[0] -= lr*error*self.data[i%self.number]
            self.b -= lr*error
        print(self.weight,self.b)






if __name__ == '__main__':
    data = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]]
    label = [2, 3.5, 6.3, 9.8, 11, 11.5, 13, 15.4, 17.2, 19]
    linear_regression = linear_regression()
    linear_regression.input(data,label,2)
    linear_regression.fit(10000,0.01)
