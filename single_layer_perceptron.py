import numpy as np

class NN:
    def __init__(self):
        self.w1 = 0
        self.w2 = 0
        self.w0 = 0
        self.lr = 0.01

    def loss(self, predicted, correct):
        return (predicted-correct)**2

    def gradient(self, dp, prediction, label):
        del_w1 = 2*(prediction-label)*(dp[0])
        del_w2 = 2*(prediction-label)*(dp[1])
        del_w0 = 2*(prediction-label)
        return del_w0, del_w1, del_w2

    def predict(self, dp):
        p = self.w1*dp[0]+self.w2*dp[1]+self.w0
        # return 1/(1+np.exp(-1*p))
        return p
        # if p>0:
        #     return 1
        # else:
        #     return 0

    def train(self, dataset, labelset):
        for i in range(len(dataset)):
            data = dataset[i]
            label = labelset[i]
            prediction = self.predict(data)
            g0, g1, g2 = self.gradient(data, prediction, label)          
            
            self.w1 -= self.lr * g1
            self.w2 -= self.lr * g2
            self.w0 -= self.lr * g0

            print(f"w1: {self.w1}, w2: {self.w2}, w0:{self.w0}")

dataset = np.array([[0,0], [0,1], [1,0], [1,1]])
labelset = np.array([0,1,1,1])

p = NN()
epochs = 10000
for i in range(epochs):
    p.train(dataset, labelset)

for i in range(len(dataset)):
    data = dataset[i]
    label = labelset[i]
    print(f"{i}: {p.predict(data)}")


