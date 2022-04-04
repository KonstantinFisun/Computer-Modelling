import math
import numpy as np
import matplotlib.pyplot as plt

def runge_kutta(y, x, dx, f):
    k1 = dx * f(y, t)
    k2 = dx * f(y + 0.5 * k1, x + 0.5 * dx)
    k3 = dx * f(y + 0.5 * k2, x + 0.5 * dx)
    k4 = dx * f(y + k3, x + dx)

    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.

def main()
    t = 0.
    y = 1.
    dt = .1
    ys, ts = [], []

    def func(y, t):
        return t * math.sqrt(y)

    while t <= 10:
        y = runge_kutta(y, t, dt, func)
        t += dt
        ys.append(y)
        ts.append(t)

    plt.plot(ts, ys, label='Метод Рунге-Кутта')
    plt.legend()
    plt.show()

if __name__=='__main__':
    main()
