import numpy as np
import matplotlib.pyplot as plt

def act(x):
    return 0 if x < 0 else 1

def forward(x, w):
    s = np.dot(w,x)
    y = [act(a) for a in s]
    return y

def fin(promejnost):
    s=[]
    for i in range (n):
        if ((promejnost[0][i] + promejnost[1][i] + promejnost[2][i] + promejnost[3][i] + promejnost[4][i] + promejnost[5][i]) / 2) == 1.5:
            s.append(1)
        else:
            s.append(0)
    return s

n = 75
x1 = np.random.random(n)
x2 = np.random.random(n)
x3 = [1] * n
X = np.array([x1,x2,x3])

w1 = np.array([1,1,-1.5])
w2 = np.array([1,1,-0.5])
w3 = np.array([1,-1,-0.5])
w4 = np.array([1,-1,0.5])
w5 = np.array([1,0,-0.2])
w6 = np.array([1,0,-0.8])

promejnost1 = forward(X,w1)
promejnost2 = forward(X,w2)
promejnost3 = forward(X,w3)
promejnost4 = forward(X,w4)
promejnost5 = forward(X,w5)
promejnost6 = forward(X,w6)

promejnost=np.array([promejnost1, promejnost2, promejnost3, promejnost4, promejnost5, promejnost6])

result=(fin(promejnost))
print(result)


a = [0.5, 0.8]
b = [1 ,0.7]
plt.plot(a, b, c="blue")
a = [0.8, 0.8]
b = [0.7, 0.3]
plt.plot(a, b, c="blue")
a = [0.8, 0.5]
b = [0.3, 0]
plt.plot(a, b, c="blue")

a = [0.2, 0.2]
b = [0.3, 0.7]
plt.plot(a, b, c="blue")
a = [0.2, 0.5]
b = [0.3, 0]
plt.plot(a, b, c="blue")
a = [0.5, 0.2]
b = [1, 0.7]
plt.plot(a, b, c="blue")



for i in range(n):
    if result[i] == 1:
        plt.scatter(x1[i],x2[i],c="green")
    else:
        plt.scatter(x1[i],x2[i],c="red")

plt.show()



# программа создает и визуализирует некоторый простой нейронный персептрон для двух входных переменных (x1 и x2)
