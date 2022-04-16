import numpy as np
import random
import matplotlib.pyplot as plt


class Model_detail:
    # Конструктор
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

        self.result_time = 0  # Время, которое было потрачено на всю работу
        self.time_every_detail = [0] * count_detail  # Время затраченное на каждую деталь

        self.count_breakdown = 0  # кол-во поломок

        self.count_detail = count_detail  # кол-во деталей

    # Обработчик деталей
    def model(self):

        count_processed_detail = 0  # количество деталей, которые были обработаны
        number_detail = 0  # Номер детали в очереди

        check_breakdown = True  # Станок в любой момент может сломаться
        all_time_breakdown = 0  # суммарное время поломок
        all_time_interval_next = 0 # Суммарное время всего ожидания

        time_between_breakdown = 0  # время между поломками
        time_for_this_detail = 0  # Время выполнения текущей детали

        again = 0  # Флаг

        # если деталей обработано меньше чем дано или есть деталей нет в очереди
        while count_processed_detail < self.count_detail:
            again = 0  # Флаг

            # Получаем детали с интервалом, пока не получим все:
            if number_detail < self.count_detail:
                time_interval_next = random.expovariate(1)  # экспоненциальное распределение
                all_time_interval_next += time_interval_next

                # Если это первая деталь, то прибавляем время ожидания, иначе отнимаем время ожидания других
                if count_processed_detail == 0:
                    self.time_every_detail[count_processed_detail] += time_interval_next  # Добавили время ожидания
                else:
                    # Если предыдущая деталь обработалась
                    if time_for_this_detail == 0:
                        # Если у нас есть время ожидания
                        if all_time_interval_next - self.result_time > 0:
                            self.time_every_detail[count_processed_detail] += all_time_interval_next - self.result_time  # Добавили время ожидания
                        else:
                            self.time_every_detail[count_processed_detail] = 0 # Ожидания не было



            # Наладка станка:
            install_machine = np.random.uniform(self.min_setup_time, self.max_setup_time)

            time_for_this_detail += install_machine  # Прибавляем время наладки

            # Время выполнения текущей детали
            time_work_machine = np.random.normal(self.mx_time, self.sd_time)  # нормальное распределение

            # если интервал следующей поломки не выбран:
            if check_breakdown:
                # Время следующей поломки
                time_between_breakdown = np.random.normal(self.interval_breaking, self.sd_interval_breaking)
                check_breakdown = False  # Станок скоро сломается

            # Поломка произошла, когда обрабатывалась деталь:
            if time_for_this_detail + self.result_time + time_work_machine + self.time_every_detail[count_processed_detail] > \
                    all_time_breakdown + time_between_breakdown > time_for_this_detail + self.result_time + self.time_every_detail[count_processed_detail]:

                # Время устранения поломки
                time_fix_breakdown = np.random.uniform(self.min_breakdown_duration, self.max_breakdown_duration)  # равномерное распределение

                time_for_this_detail += time_fix_breakdown + \
                                        (all_time_breakdown + time_between_breakdown - time_for_this_detail - self.result_time)  # Добавили время исправления детали и время работы станка

                all_time_breakdown += time_between_breakdown + time_fix_breakdown  # сохраняем интервал и время на починку

                self.count_breakdown += 1  # Отмечаем поломку

                check_breakdown = True  # Станок починили

                again = 1  # Обработка детали заново

            # Поломка произошла во время простоя:
            elif time_for_this_detail + time_work_machine + self.result_time + self.time_every_detail[count_processed_detail] > all_time_breakdown + time_between_breakdown > self.result_time:

                # Время устранения поломки
                time_fix_breakdown = np.random.uniform(self.min_breakdown_duration,
                                                       self.max_breakdown_duration)  # равномерное распределение

                all_time_breakdown += time_between_breakdown + time_fix_breakdown  # сохраняем интервал и время на починку

                time_for_this_detail += time_work_machine  # деталь полноценно обработалась

                self.count_breakdown += 1  # отмечаем поломку

                check_breakdown = True  # станок починили
            #Если поломок не было
            else :
                time_for_this_detail += time_work_machine

            # еще одна деталь готова
            if again == 0:
                self.time_every_detail[count_processed_detail] += time_for_this_detail  # Добавляем время обработки детали
                self.result_time += self.time_every_detail[count_processed_detail]
                # print("Время выполнения с учетом ожидания:" + str(count_processed_detail) + " номер "
                #       + str(self.time_every_detail[count_processed_detail]) + " время ")
                # print("Количество поломок: " + str(self.count_breakdown))
                # print()

                time_for_this_detail = 0 # Обновляем время
                count_processed_detail += 1  # Деталь готова

    # Вывод
    def output(self):
        print('Общее время выполнения задачи: ' + str(self.result_time) + ' ч.')
        print("Количество поломок: " + str(self.count_breakdown))


    # График
    def show(self):
        plt.hist(self.time_every_detail, color='blue', edgecolor='black',
                 bins=int(self.count_detail / 10))

        plt.title('Время затраченное на каждую деталь')
        plt.xlabel('Время ч.')
        plt.ylabel('Количество деталей')
        plt.show()


def main():
    a = Model_detail(500)
    a.model()
    a.output()
    a.show()


if __name__ == '__main__':
    main()
