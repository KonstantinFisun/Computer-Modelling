import matplotlib.pyplot as plt
import numpy as np

b = 2  # правая граница t


# точные решение для 1 задачи
# x = 4e(-t)-e(2t)
def exact_x1(t):
    return 4 * np.exp(-t) - np.exp(2 * t)


# y = e(-t)-e(2t)
def exact_y1(t):
    return np.exp(-t) - np.exp(2 * t)


# точные значения для 2 задачи
# x = e(2t)+1
def exact_x2(t):
    return np.exp(2 * t) + 1


# y = 2e(2t)
def exact_y2(t):
    return 2 * np.exp(2 * t)


# производные из 1 задачи
# x'=-2x+4y, x(0)=3
def fun_x1(t, x, y):  # x(t)
    return -2 * x + 4 * y


# y'=-x+3y, y(0)=0
def fun_y1(t, x, y):  # y(t)
    return -x + 3 * y


# производные из 2 задачи
# x'=y, x(0)=2
def fun_x2(t, x, y):
    return y


# y'=2y, y(0)=2
def fun_y2(t, x, y):
    return 2 * y


# считает коэффициенты для функций
# fun_x - производная по x
# fun_y - производная по y
# h - шаг
def formula(fun_x, fun_y, t, x, y, h):
    k1 = h * fun_x(t, x, y)
    l1 = h * fun_y(t, x, y)

    k2 = h * fun_x(t + h / 2, x + k1 / 2, y + l1 / 2)
    l2 = h * fun_y(t + h / 2, x + k1 / 2, y + l1 / 2)

    k3 = h * fun_x(t + h / 2, x + k2 / 2, y + l2 / 2)
    l3 = h * fun_y(t + h / 2, x + k2 / 2, y + l2 / 2)

    k4 = h * fun_x(t + h, x + k3, y + l3)
    l4 = h * fun_y(t + h, x + k3, y + l3)

    d_x = (k1 + 2 * k2 + 2 * k3 + k4) / 6
    d_y = (l1 + 2 * l2 + 2 * l3 + l4) / 6

    return d_x, d_y


def runge_kutta_4(fun_x, fun_y, x0, y0, h, t0):  # Метод Рунге-Кутта 4 - го порядка
    # начальные значения
    x = [x0]
    y = [y0]
    t = [t0]

    # заполнение массивов координат
    for i in range(20):
        d_x, d_y = formula(fun_x, fun_y, t0, x0, y0, h)
        x0 = x0 + d_x  # функция x(t)
        y0 = y0 + d_y  # функция y(t)
        t0 = t0 + h
        x.append(x0)
        y.append(y0)
        t.append(t0)

    return x, y, t


# вычисление точных значений x(t), y(t)
def exact_solution(exact_x, exact_y, t0):
    N = 100
    x, y = [], []
    t = np.linspace(t0, N)
    for i in t:
        x.append(exact_x(i))
        y.append(exact_y(i))
    return x, y, t


# построение графиков
def show(fun_x, fun_y, exact_x, exact_y, x0, y0, t0, title):
    x, y, t = runge_kutta_4(fun_x, fun_y, x0, y0, 0.1, t0)  # Решение с помощью Рунге-Кутта
    x1, y1, t1 = exact_solution(exact_x, exact_y, t0)  # Точное решение

    fig, ax = plt.subplots()
    ax.plot(t1, x1, label='Точное решение, x(t)')
    ax.plot(t1, y1, label='Точное решение, y(t)')

    ax.plot(t, x, label='Метод Рунге-Кутта \nчетвертого порядка, x(t)', linestyle='-.')
    ax.plot(t, y, label='Метод Рунге-Кутта \nчетвертого порядка, y(t)', linestyle='-.')

    ax.legend(fontsize=12, ncol=2, facecolor='oldlace', edgecolor='r', title_fontsize='14')

    plt.title(title)
    plt.show()


def main():
    # Первая задача
    show(fun_x1, fun_y1, exact_x1, exact_y1, 3, 0, 0, "Задание 1")
    # Вторая задача
    # show(fun_x2, fun_y2, exact_x2, exact_y2, 2, 2, 0, "Задание 2")


if __name__ == '__main__':
    main()
