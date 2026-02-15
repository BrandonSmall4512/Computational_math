import matplotlib.pyplot as plt
import numpy as np

def func(x):
    return 0.08 * x**3 - 1.3 * x - 5.4                

def chord_method(func, a, b, epsilon=1e-6, max_iterations=1000):
    # проверка на перегиб
    if func(a) * func(b) >= 0:
        print("На заданном интервале функция не меняет знак, метод может не сработать")
        return None

    iterations = 0
    c = a - (b - a) * func(a) / (func(b)-func(a))
    
    while abs(b - a) > epsilon and iterations < max_iterations:

        if np.abs(func(c)) < epsilon:
            break
        elif func(a) * func(c) < 0:
            b = c
        else:
            a = c

        c = a - (b - a) * func(a) / (func(b) - func(a))
        iterations += 1

    return c, iterations

def midpoint_method(func, a, b, epsilon=1e-9, max_iterations=1000):
    # проверка на перегиб
    if func(a) * func(b) >= 0:
        print("На заданном интервале функция не меняет знак, метод может не сработать")
        return None

    iterations = 0
    while abs(b - a) > epsilon: # and iterations < max_iterations:

        # функция получения новой границы интервала
        c = (a + b) / 2

        if func(c) == 0:
            return c
        elif func(a) * func(c) < 0:
            b = c
        else:
            a = c
        iterations += 1

    return (a + b) / 2, iterations


a, b = -1, 18
epsilon = 1e-6

# Находим корень методом хорд
root1, iterations1 = chord_method(func, a, b, epsilon)

if root1 is not None:
    print(f"Нуль функции на интервале [{a}, {b}] методом хорд: {root1}")
    print(f"Количество итераций{iterations1}")
else:
    print("Не удалось найти нуль функции на заданном интервале методом хорд")

a, b = -1, 18
epsilon = 1e-6



root2, iterations2 = midpoint_method(func, a, b, epsilon)

if root2 is not None:
    print(f"Нуль функции на интервале [{a}, {b}] методом хорд: {root2}")
    print(f"Количество итераций{iterations2}")
else:
    print("Не удалось найти нуль функции на заданном интервале методом хорд")

x = np.linspace(a, b, 1000)
y = func(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y, label='f(x) = x^3 - 2x - 5') 
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(root2, color='red', linestyle='--', label='Нуль функции - 1')
plt.title('График функции')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()


