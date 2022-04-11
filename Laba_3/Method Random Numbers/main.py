import numpy as np
import matplotlib.pyplot as plt


# Метод квадратов
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
        if capacity % 2 == 0:
            new_num = num_2[int(capacity - capacity / 2):int(capacity + capacity / 2)]  # Если четное число разрядов
        else:
            new_num = num_2[int(capacity - capacity / 2):int(capacity + capacity / 2)]

        # Добавляем случайное число,
        # равномерно распределённое в интервале (0; 1);
        random_number = np.append(random_number, int(new_num) * pow(10, -capacity))

        num = new_num

    plt.hist(random_number, color='blue', edgecolor='black',
             bins=int(n / 10))

    plt.title('Гистограмма метода квадратов')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.show()

    return random_number


# Метод произведений
def method_compasion(num, core, n):
    # Массив полученных чисел
    random_number = np.array([])
    capacity = len(num)  # Разрядность числа
    for i in range(n):

        num_2 = str(int(num) * core)  # Число на ядро

        # Добавление незначущих нулей
        while len(num_2) != capacity * 2:
            num_2 = "0" + num_2

        # Выделяем n средних разрядов
        if capacity % 2 == 0:
            new_num = num_2[int(capacity - capacity / 2):int(capacity + capacity / 2)]  # Если четное число разрядов
        else:
            new_num = num_2[int(capacity - capacity / 2):int(capacity + capacity / 2)]

        # Добавляем случайное число,
        # равномерно распределённое в интервале (0; 1);
        random_number = np.append(random_number, int(new_num) * pow(10, -capacity))

        num = num_2[-capacity:]

    plt.hist(random_number, color='blue', edgecolor='black',
             bins=int(n / 10))

    plt.title('Гистограмма метода произведений')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.show()

    return random_number


# Мультипликативный конгруэнтный метод
def multiplicative_congruent_method(num, multiplier, divider, n):
    # Массив полученных чисел
    random_number = np.array([])
    capacity = len(str(num))  # Разрядность числа
    for i in range(n):
        new_num = (num * multiplier + 0) % divider  # Число на множитель и получаем остаток
        capacity = len(str(num))
        # Добавляем случайное число,
        # равномерно распределённое в интервале (0; 1);
        pull = len(str(new_num))
        random_number = np.append(random_number, new_num * pow(10, -pull))

        num = new_num
    plt.hist(random_number, color='blue', edgecolor='black',
             bins=int(n / 10))

    plt.title('Гистограмма мультипликативного конгруэнтного метода')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.show()

    return random_number


# методы, представляющие модификации перечисленных методов
def multiplicative_congruent_method_modification(num, multiplier, divider, n, u):
    # Массив полученных чисел
    random_number = np.array([])
    capacity = len(str(num))  # Разрядность числа
    for i in range(n):
        new_num = ((num * multiplier) + u) % divider  # Число на множитель и получаем остаток
        capacity = len(str(num))
        # Добавляем случайное число,
        # равномерно распределённое в интервале (0; 1);
        pull = len(str(new_num))
        random_number = np.append(random_number, new_num * pow(10, -pull))

        num = new_num

    plt.hist(random_number, color='blue', edgecolor='black',
             bins=int(n / 10))

    plt.title('Гистограмма метода, представляющий модификацию перечисленных методов')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.show()

    return random_number


def main():
    n = 1000  # Количество повторений
    # num = 7153 # Исходное число
    # method_square(str(num), n)
    #
    # num = 3729  # Исходное число
    # core = 5167 # Ядро
    # method_compasion(str(num), core, n)

    num = 1357 # Исходное число
    multiplier = 1357 # Множитель
    divider = 5689 # Делитель
    multiplicative_congruent_method(num, multiplier, divider, n)

    num = 1357  # Исходное число
    multiplier = 1357  # Множитель
    divider = 5689  # Делитель
    u = 39999999999999999  # Аддитивная константа
    multiplicative_congruent_method_modification(num, multiplier, divider, n, u)


if __name__ == '__main__':
    main()
