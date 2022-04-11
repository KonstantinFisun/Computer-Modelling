import numpy as np
import random


class Model1:
    def __init__(self, count_detail):

        # Наладка станка 0.2 до 0.5 ч
        self.min_setup_time = 0.2  # время наладки станка(миним)
        self.max_setup_time = 0.5  # время наладки станка(макс)

        # Время выполнения 0.5 ч с среднеквадратичным отклонением 0.1 ч
        self.mx_time = 0.5  # мат ожидание времени выполнения задания
        self.sd_time = 0.1  # сред кв откл времени выполнения задания

        # Интервал между поломками 20 ч и среднеквадратичным отклонение 2 ч
        self.interval_breaking = 20  # мат ожидание интервалов между поломками
        self.sd_interval_breaking = 2  # сред кв откл  интервалов между поломками

        # Продолжительность поломки на интервале 0.1 до 0.5 равномерно
        self.min_breakdown_duration = 0.1  # время устранения поломки станка(миним)
        self.max_breakdown_duration = 0.5  # время устранения поломки станка(макс)

        self.count_detail = count_detail  # кол-во деталей

    def model(self):
        det = 0  # количество деталей, которые были обработаны
        res_time = 0  # время, которое было потрачено на всю работу (500 деталей)
        check_breakdown = True  # изначально время поломки станка неизвестно. Если false, то до/во время изготовления предыдущей детали станок не успел сломаться, но может сломаться потом
        sum_t_breakdown = 0  # суммарное время поломок
        count_breakdown = 0  # кол-во поломок
        t_breakdown = 0  # время между поломками
        queue = []  # очередь деталей

        while det < self.count_detail or len(queue) != 0:  # если деталей не 500 или есть деталей нет в очереди
            time_for_this_det = res_time  # будем работать со временем в безопасной переменной

            # перед выполнением каждого задания нужна наладка станка:
            t_naladki = np.random.uniform(self.min_setup_time, self.max_setup_time)

            # ЕСЛИ ЭТО УБРАТЬ, ТО ОТВЕТ СХОДИТСЯ:???
            time_for_this_det += t_naladki  # но я считаю, что с наладкой ответ правильнее

            # получаем деталь с интервалом:
            t_interval_next = random.expovariate(1)  # экспоненциальное распределение

            # время выполнения текущего задания
            t_work = np.random.normal(self.mx_time,
                                      self.sd_time)  # нормальное распределение
            time_for_this_det += t_interval_next

            # если интервал следующей поломки не выбран:
            if check_breakdown:
                t_breakdown = np.random.normal(self.interval_breaking,
                                               self.sd_interval_breaking)
                check_breakdown = False  # станок надо чинить скоро

            # Поломка произошла, когда обрабатывалась деталь:
            if time_for_this_det + t_work > sum_t_breakdown + t_breakdown > time_for_this_det:

                # время устранения поломки
                t_fix_breakdown = np.random.uniform(self.min_breakdown_duration,
                                                    self.max_breakdown_duration)  # равномерное распределение

                sum_t_breakdown += t_breakdown + t_fix_breakdown  # сохраняем интервал и время на починку

                time_for_this_det = sum_t_breakdown  # sum_t_breakdown полностью задает время, которое прошло с начала работы станка, потому что хранит все интервалы между поломками+время на починку каждой из них
                # это присваивание (строка выше) нужно, чтобы учесть время, которое было потрачено на незаконченную деталь

                count_breakdown += 1  # отмечаем поломку

                check_breakdown = True  # станок починили
                det += 1

                queue.append(det)  # отправка детали в очередь

            # 2) она произошла во время простоя:
            elif time_for_this_det + t_work > sum_t_breakdown + t_breakdown > res_time:
                # время устранения поломки
                t_fix_breakdown = np.random.uniform(self.min_breakdown_duration,
                                                    self.max_breakdown_duration)  # равномерное распределение

                sum_t_breakdown += t_breakdown + t_fix_breakdown  # сохраняем интервал и время на починку

                time_for_this_det += t_work  # деталь полноценно обработалась

                count_breakdown += 1  # отмечаем поломку

                check_breakdown = True  # станок починили

            # еще одна деталь готова
            if len(queue) == 0:
                det += 1
            else:
                del (queue[0])  # если была очередь, берем деталь из нее

            res_time = time_for_this_det  # сохраняем время обработки

        print('Время выполнения задания: ' + str(res_time) + ' ч.\nКоличество поломок: ' + str(count_breakdown))


def main():
    a = Model1(50000000000000000000000000000000000000)
    a.model()


if __name__ == '__main__':
    main()
