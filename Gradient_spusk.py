import numpy as np
import matplotlib.pyplot as plt


def function(x, y):
    return x**4 - 3 * x**3 + 2 * x**2 - 5*x*y + 5*y**3

def derivative_x(x, y):
    return 4 * x**3 - 9 * x**2 + 4 * x - 5 * y

def derivative_y(x, y):
    return -5*x + 15 * y**2


def gradient_descent(learning_rate, epochs):
    x = 4  
    y = 3  
    x_history = [x]
    y_history = [y]
    
    for _ in range(epochs):
        grad_x = derivative_x(x, y)
        grad_y = derivative_y(x, y)
        x = x - learning_rate * grad_x
        y = y - learning_rate * grad_y
        x_history.append(x)
        y_history.append(y)
    
    return x_history, y_history

# Параметры для градиентного спуска
learning_rate = 0.02
epochs = 10

history_x, history_y = gradient_descent(learning_rate, epochs)

print('x0 = ', history_x[-1])
print('y0 = ', history_y[-1])

z = function(history_x[-1], history_y[-1])
print('z0 = ', z)

x_vals = np.linspace(-2, 5, 100)
y_vals = np.linspace(-2, 5, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = function(X, Y)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax.scatter(history_x, history_y, [function(x, y) for x, y in zip(history_x, history_y)], c='red', label='Градиентный спуск', marker='x')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.title('Градиентный спуск по функции')
plt.legend()
plt.show()

