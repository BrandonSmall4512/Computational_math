import matplotlib.pyplot as plt
import csv
import numpy as np


def read_csv(file_path):
    x_values, y_values = [], []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            x_values.append(float(row[0].replace(',', '.')))
            y_values.append(float(row[1].replace(',', '.')))
    return x_values, y_values


def graf_len(x_v, y_v):
    x = np.unique(x_v)
    y = [np.mean([y_v[i] for i in range(len(y_v)) if x_v[i] == j]) for j in x]


    # Рассчет необходимых сумм и значений для вычисления коэффициентов a и b
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x_squared = np.sum(x**2)
    sum_xy = np.sum(x*y)

    # Вычисление коэффициентов a и b по формулам метода наименьших квадратов
    b = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    a = (sum_y - b * sum_x) / n

    print(f"Коэфицент а: {a}")
    print(f"Коэфицент b: {b}")

    # Создание функции линейной регрессии
    def linear_regression(x, a, b):
        return a + b * x

    # Построение линейной регрессии
    regression_line = linear_regression(x, a, b)

    # Визуализация результатов
    plt.scatter(x, y, label='Исходные данные')
    plt.plot(x, regression_line, 'r', label='Линейная регрессия')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Метод наименьших квадратов для линейной аппроксимации')
    plt.legend()
    plt.grid(True)
    plt.show()

    
file_path = 'INPUT.csv'
x, y = read_csv(file_path)

graf_len(x, y)


