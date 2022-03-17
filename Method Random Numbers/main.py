import math
import random
import numpy as np

# метод квадратов
def method_square(num, n):
    # Массив полученных чисел
    random_number = np.array([])
    capacity = len(num)  # Разрядность числа
    for i in range(n):

        num_2 = str(pow(int(num), 2))  # Число в квадрате

        # Добавление незначущих нулей
        while len(num_2) != capacity * 2:
            num_2 = "0" + num_2



        # Выделяем n средних разрядов
        if(capacity % 2 == 0):
            new_num = num_2[int(capacity - capacity/2):int(capacity+capacity/2)]# Если четное число разрядов
        else:
            new_num = num_2[int(capacity - capacity / 2):int(capacity + capacity / 2)]

        # Добавляем случайное число,
        # равномерно распределённое в интервале (0; 1);
        random_number = np.append(random_number, int(new_num)*pow(10,-capacity))

        num = new_num

    return random_number


def main():
    num = 1357 # Исходное число
    n = 1000 # Количество повторений
    print(method_square(str(num), n))
    # метод произведений
    # мультипликативный конгруэнтный метод
    # методы, представляющие модификации перечисленных методов

if __name__ == '__main__':
    main()

