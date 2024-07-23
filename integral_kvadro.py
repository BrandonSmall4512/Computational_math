import matplotlib.pyplot as plt
import numpy as np

def rectangle_integral(func, a, b, n, required_precision = 1e-3):

    dx = (b - a) / n

    # для хранения суммы площадей прямоугольников
    integral = 0.0

    prev_integral = float('inf')  # Инициализация предыдущего значения интеграла как бесконечности

    while abs(integral - prev_integral) > required_precision:  # Пока разница больше требуемой точности
        prev_integral = integral  # Сохраняем предыдущее значение интеграла
        integral = 0.0  # Сброс значения интеграла перед каждой итерацией

        for i in range(n):
            # Вычисление значения функции в текущей точке
            x = a + i * dx
            integral += func(x) * dx

        n *= 2  # Увеличиваем количество шагов на каждой итерации
        
        dx = (b - a) / n  # Пересчитываем шаг

    return integral


def trapezoidal_integral(func, a, b, n, required_precision = 1e-6):

    dx = (b - a) / n
    # Инициализация переменной для хранения суммы площадей трапеций
    integral = 0.0
    
    prev_integral = float('inf')  # Инициализация предыдущего значения интеграла как бесконечности
    
    while abs(integral - prev_integral) > required_precision:  # Пока разница больше требуемой точности
        prev_integral = integral  # Сохраняем предыдущее значение интеграла
        integral = 0.0  # Сброс значения интеграла перед каждой итерацией

        for i in range(n):
            x0 = a + i * dx
            x1 = a + (i + 1) * dx
            integral += (func(x0) + func(x1)) * dx / 2

        n *= 2  # Удваиваем количество шагов на каждой итерации
        
        dx = (b - a) / n  # Пересчитываем шаг

    return integral


def simpson_integral(func, a, b, n, required_precision=1e-6):
    dx = (b - a) / n
    sum_f = func(a) + func(b)
    integral = sum_f

    prev_integral = float('inf')  # Инициализация предыдущего значения интеграла как бесконечности
    
    while abs(integral - prev_integral) > required_precision:
        prev_integral = integral
        integral = 0.0
        sum_f = 0.0  # Сброс суммы значений функции в узлах

        for i in range(1, n, 2):  # Используем только нечетные индексы для узлов
            x = a + i * dx
            sum_f += 4 * func(x)

        for i in range(2, n-1, 2):  # Используем только четные индексы для узлов
            x = a + i * dx
            sum_f += 2 * func(x)

        integral = (func(a) + func(b) + sum_f) * dx / 3
        n *= 2
        dx = (b - a) / n

    return integral


# Пример использования функции для интегрирования x^2 от 0 до 1
def f(x):
    return -x**5 + 5.4 * x**4 - 1.2 * x**3 - 1.5 *x**2 - 1.5 * x - 25




# Задание пределов интегрирования и количества прямоугольников
a = -3
b = 4
n = 100

# Вычисление интеграла методом прямоугольников
result = rectangle_integral(f, a, b, n)
print("Результат интегрирования:", result)

# Вычисление интеграла методом трапеции
result = trapezoidal_integral(f, a, b, n)
print("Результат интегрирования:", result)

# Вычисление интеграла методом Симпсона
result = simpson_integral(f, a, b, n)
print("Результат интегрирования:", result)

# Визуализация функции
x_vals = np.linspace(a, b, 100)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals, label='f(x) = x^2')
plt.fill_between(x_vals, y_vals, color='skyblue', alpha=0.4)
plt.title('График функции и метода прямоугольников')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.show()

