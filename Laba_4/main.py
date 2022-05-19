import matplotlib.pyplot as plt
import numpy as np

# x' = -2x + 4y, x(0) = 3
# y' = -x + 3y, y(0) = 0
def funX1(t, x, y):
    return -2*x + 4*y

def funY1(t, x, y):
    return -x + 3*y

# x' = y, x(0) = 2
# y' = 2y, y(0) = 2
def funX2(t,x,y):
    return y

def funY2(t, x, y):
    return 2*y

# Точные значения для 1 задания
def exactValueX1(t):
    return 4 * np.exp(-t)-np.exp(2*t)

def exactValueY1(t):
    return np.exp(-t)-np.exp(2*t)

# Точные значения для 2 задания
def exactValueX2(t):
    return np.exp(2*t) + 1

def exactValueY2(t):
    return 2 * np.exp(2*t)

# Вычисление точных значений x(t), y(t)
def exactValuesCalculation(exactValueX, exactValueY, t0, b):
    N = 100
    x,y = [],[]
    t = np.linspace(t0, b, N)

    for i in t:
        x.append(exactValueX(i))
        y.append(exactValueY(i))

    return x, y, t


# Считает коэффициенты для двух функций (11 стр)
def deltaXY(funX, funY, t, x, y, step):
    k1 = step * funX(t, x, y)
    l1 = step * funY(t, x, y)

    k2 = step * funX(t + step / 2, x + k1 / 2., y + l1 / 2.)
    l2 = step * funY(t + step / 2, x + k1 / 2., y + l1 / 2.)

    k3 = step * funX(t + step / 2, x + k2 / 2., y + l2 / 2.)
    l3 = step * funY(t + step / 2, x + k2 / 2., y + l2 / 2.)

    k4 = step * funX(t + step, x + k3, y + l3)
    l4 = step * funY(t + step, x + k3, y + l3)

    deltaX = (k1 + 2. * k2 + 2.* k3 + k4)/6
    deltaY = (l1 + 2. * l2 + 2. * l3 + l4)/6
    return deltaX, deltaY

def methodCalculation(funX, funY, x0, y0, h, t0, b):
    # Начальные значения
    x = [x0]
    y = [y0]
    t = [t0]

    # Заполнение массивов координат
    for i in range(20):
        deltaX,deltaY = deltaXY(funX, funY, t0, x0, y0, h)
        # Функция x(t)
        x0 = x0 + deltaX
        # Функция y(t)
        y0 = y0 + deltaY
        t0 = t0 + h

        x.append(x0)
        y.append(y0)
        t.append(t0)

    return x, y, t

# Построение графиков
def plotting(funX, funY, exactValueX, exactValueY, x0, y0, t0, b, lim1, lim2, h):
    x, y, t = methodCalculation(funX, funY, x0, y0, h, t0, b)
    exactX, exactY, exactT = exactValuesCalculation(exactValueX, exactValueY, t0, b)

    fig, ax = plt.subplots()
    ax.plot(exactT, exactX, label = 'Точное решение x(t)', linewidth=5, color='green')
    ax.plot(exactT, exactY, label = 'Точное решение y(t)', linewidth=5, color='red')

    ax.plot(t, x, label='По методу Рунге-Кутта 4-го порядка, x(t)', color='black')
    ax.plot(t, y, label='По методу Рунге-Кутта 4-го порядка, y(t)', color='yellow')
    ax.legend(fontsize = 12, ncol = 2, facecolor = 'oldlace', edgecolor='black', title_fontsize = '12')

    plt.ylim(lim1, lim2)
    fig.set_figwidth(8)
    fig.set_figheight(4)
    fig.tight_layout() # Убираем пустое пространство
    plt.show()

if __name__ == '__main__':
    # Правая граница t
    b = 2
    # Шаг
    h = 0.1
    plotting(funX1, funY1, exactValueX1, exactValueY1, 3, 0,0,b, -10, 10, h)
    plotting(funX2, funY2, exactValueX2, exactValueY2, 2, 2,0,b, -2, 10, h)