import numpy as np
import matplotlib.pyplot as plt

# Функция для решения системы линейных уравнений методом прогонки
def solve_tridiagonal(a, b, c, d):
    n = len(d)
    c_dash = np.zeros(n - 1)
    d_dash = np.zeros(n)
    x = np.zeros(n)

    # Прямой ход прогонки
    c_dash[0] = c[0] / b[0]
    d_dash[0] = d[0] / b[0]

    for i in range(1, n - 1):
        c_dash[i] = c[i] / (b[i] - a[i - 1] * c_dash[i - 1])

    for i in range(1, n):
        d_dash[i] = (d[i] - a[i - 1] * d_dash[i - 1]) / (b[i] - a[i - 1] * c_dash[i - 1])

    # Обратный ход прогонки
    x[-1] = d_dash[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_dash[i] - c_dash[i] * x[i + 1]

    return x

# Пример использования для решения уравнения y'' = -y^2 + x*y - 2
# с начальными условиями y(0) = 0 и y'(0) = 1 на интервале [0, 5]

# Задаем количество узлов
n = 101  # Увеличим количество узлов для более точного решения

# Создаем массивы для коэффициентов трехдиагональной матрицы
a = np.ones(n - 1)
b = np.zeros(n)
c = np.ones(n - 1)
d = np.zeros(n)

# Шаг по x
h = 5.0 / (n - 1)

# Начальные условия
d[0] = 0.0
d[1] = 1.0

# Заполняем коэффициенты матрицы и вектора d
for i in range(1, n - 1):
    b[i] = -2 - h**2 + i * h
    d[i + 1] = -2 * h**2

b[0] = -2 - h**2
b[-1] = -2 - h**2 + (n - 1) * h

solution = solve_tridiagonal(a, b, c, d)

# Создаем массив для значений x
x_values = np.linspace(0, 5, n)

# Выводим результаты
for i, sol in enumerate(solution):
    print(f"y({i * h:.2f}) = {sol:.6f}")


# Строим график
plt.figure(figsize=(8, 6))
plt.plot(x_values, solution, label='Решение уравнения')
plt.xlabel('x')
plt.ylabel('y')
plt.title("Решение дифференциального уравнения y'' = -y^2 + x*y - 2")
plt.legend()
plt.grid(True)
plt.show()


