import numpy as np
import warnings
from matplotlib import pyplot as plt
class least_square():
    def __init__(self):
        self.number = 2
        self.data = []
        self.datax = []
        self.label = []
        self.labely = []
        self.p = 0
        self.prediction = []
    def fit_function_number(self,x):
        if x < 2 or int(x) != x:
            raise Exception("fit_function's Number can't be this:(Int and larger than 1)", x)
        self.number = x
    def input_data(self,data,label):
        self.datax = data
        self.labely = label
        data_memroy = []
        xdata_memroy = []
        for a in range(len(data)):
            xdata_memroy = []
            for b in range(self.number):
                xdata_memroy.append(data[a]**b)
            data_memroy.append(xdata_memroy)
        self.data = np.array(data_memroy)
        self.label = np.array([label]).T
    def fit(self):
        self.p = np.linalg.inv(self.data.T.dot(self.data))*(self.data.T.dot(self.label))
        prediction = np.zeros((len(self.p),self.number))
        for a in range(len(self.p)):
            prediction += self.p[a]
        self.prediction = prediction[0]
        print(self.prediction)
        warnings.warn('Result is from b-->kn')
        return prediction[0]
    def predict(self,x):
        result = 0
        for i in range(self.number):
            result += self.prediction[i] * (x**i)
        return result
if __name__ == '__main__':
    least_square = least_square()
    x = [1,2,3,4,5]
    y = [7,13,28,40,68]
    least_square.fit_function_number(10)
    least_square.input_data(x,y)
    a = least_square.fit()
    plt.scatter(x,y)
    x1 = np.linspace(1,5,200)
    y1 = least_square.predict(x1)
    plt.plot(x1,y1)
    plt.show()





