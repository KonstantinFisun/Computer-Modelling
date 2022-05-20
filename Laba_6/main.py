import wx  # Импортируем пакет для работы с wxPython.
import random
import PySimpleGUI as sg

class Model_lab6:
    def __init__(self, kol, n, t1, t1_r, t2, t2_r, t3, t3_r, p1, p2, p3, p1_2, p1_3, interv, interv_r):
        self.kol = int(kol) # Количество повторей
        self.n = int(n) # Количество заданий
        # Времена обработки
        self.t1 = float(t1)
        self.t1_range = float(t1_r)
        self.t2 = float(t2)
        self.t2_range = float(t2_r)
        self.t3 = float(t3)
        self.t3_range = float(t3_r)
        # Общии вероятности попадания детали
        self.p1 = float(p1)
        self.p2 = float(p2)
        self.p3 = float(p3)
        # Вероятность поступления после обработки первой ЭВМ
        self.p1_2 = float(p1_2)
        self.p1_3 = float(p1_3)
        # Интервал между заданиями
        self.interv = float(interv)
        self.interv_range = float(interv_r)

    # Выбираем интервал
    def choose_t(self, evm):
        if evm == 0:
            return random.uniform(self.t1 - self.t1_range, self.t1 + self.t1_range)
        elif evm == 1:
            return random.uniform(self.t2 - self.t2_range, self.t2 + self.t2_range)
        elif evm == 2:
            return random.uniform(self.t3 - self.t3_range, self.t3 + self.t3_range)

    def model(self):
        # Открываем файл для записи
        global t1, t2
        f = open('result.txt', 'w')
        res_t_interval = 0 # Общее время обработки
        res = [0, 0, 0] # Результат
        done_exs = [0, [0, 0], [0, 0]] # Обработано заданий
        queue = [[], [], []] # Очередь
        temp_n = 0 # Обработано заданий
        time = [0, 0, 0] # Время обработки заданий
        interval = 0 # Интервал
        max_len_queue = [0, 0, 0] # Максимальная длина в очереди
        all_in_queue = [0, 0, 0] # Всего в очереди было
        sred_t_in_queue = [0, 0, 0] # Среднее время в очереди


        while temp_n < self.n:
            t1 = 0
            t2 = [0, 0, 0]

            # Получение интервала до задания A
            if temp_n > 0:
                interval = random.uniform(self.interv - self.interv_range, self.interv + self.interv_range)

            res_t_interval += interval # Прибавляем к общему времени

            # Поступление задания A в систему
            # Взвешенный случайный выбор
            evm = random.choices([0, 1, 2], weights=[self.p1, self.p2, self.p3])[0]
            f.write("\nЭВМ " + str(evm + 1) + "")

            f.write("Интервал до этого задания: " + str(interval))
            to_queue = False # В очередь никого

            # Предыдущие задание обрабатывается или очередь не пустая
            if res[evm] > res_t_interval or queue[evm] != []:
                # Задание добавляется в очередь
                queue[evm].append((1, res_t_interval))
                f.write("\nВ очередь")
                to_queue = True # Очередь есть
                all_in_queue[evm] += 1 # Всего в очереде
                # Определение максимальной длины очереди
                if len(queue[evm]) > max_len_queue[evm]:
                    max_len_queue[evm] = len(queue[evm])
            else:
                # Обработка задания
                t1 = self.choose_t(evm) # Время обработки задания в минутах
                f.write("\nВремя обработки задания: " + str(t1))
                time[evm] += t1 # Добавляем время обработки

                # Если это первая ЭВМ
                if evm == 0:
                    done_exs[evm] += 1 # Добавляем обработанное задание к 1
                else:
                    done_exs[evm][0] += 1 # Добавляем обработанное задание к остальным
                    temp_n += 1 # Всего обработанно
                f.write("\nНе из очереди")
                res[evm] = res_t_interval + t1 # Общее время для ЭВМ

            # Проходимся по каждому ЭВМ
            for i in [0, 1, 2]:
                # Если у нас не обработалось поставленное количество деталей и очередь не пустая и ЭВМ свободна
                if temp_n < self.n and queue[i] != [] and res[i] < res_t_interval:
                    # Получение задания Bi из очереди и получаем его время обработки
                    t2[i] = self.choose_t(i)
                    f.write("\nВремя обработки задания, которое выполняется параллельно на " + str(i + 1) + ": " + str(t2[i]))
                    time[i] += t2[i] # Добавляем к времени
                    res[i] += t2[i] # Добавляем к результирующему

                    if queue[i][0][0] == 2:
                        done_exs[i][1] += 1

                    sred_t_in_queue[i] += res_t_interval - queue[i][0][1] # Отнимаем от среднего в очереди
                    del (queue[i][0]) # Убираем из очереди

                    # Если это не первая ЭВМ
                    if i != 0:
                        done_exs[i][0] += 1 # Добавляем что это первый обработал
                        temp_n += 1 # Всего обработано
                    # Если это первая ЭВМ
                    else:
                        done_exs[i] += 1 # Добавляем обработанное задание
                        # Выбор ЭВМ для обработки Bi
                        evm2_p = random.choices([1, 2], weights=[self.p1_2, self.p1_3])[0]


                        f.write("\nВедется работа на " + str(evm2_p + 1))

                        # Если ЭВМ занята
                        if res[evm2_p] > res_t_interval - interval + t1:
                            f.write("\nВ очередь")
                            # Добавляем в очередь
                            queue[evm2_p].append((2, res_t_interval))
                            all_in_queue[evm2_p] += 1 # Всего в очереди
                            # Вычисляем максимальную длину очереди
                            if len(queue[evm2_p]) > max_len_queue[evm2_p]:
                                max_len_queue[evm2_p] = len(queue[evm2_p])
                        # ЭВМ не занята
                        else:
                            # Время обработки вычисляем
                            t21 = self.choose_t(evm2_p)
                            f.write("\nВремя обработки задания: " + str(t21))
                            # Добавляем задание к обработанным
                            done_exs[evm2_p][1] += 1
                            done_exs[evm2_p][0] += 1
                            time[evm2_p] += t21 # Добавляем время обработки
                            res[evm2_p] = res_t_interval - interval + t2[i] + t21 # Общее время
                            temp_n += 1 # Добавляем к обработанным заданиям
                            t2[i] += t21 #Время работы
            # Задание обрабатывалось на 1 ЭВМ
            if evm == 0 and to_queue == False:
                # Выбираем следующую ЭВМ после 1
                evm2 = random.choices([1, 2], weights=[self.p1_2, self.p1_3])[0]
                f.write("\nРабота над заданием A после ЭВМ 1 на " + str(evm2 + 1))
                # Если ЭВМ занята
                if res[evm2] > res_t_interval + t1:
                    # Добавление в очередь
                    f.write("\nВ очередь задание А")
                    queue[evm2].append((2, res_t_interval))
                    all_in_queue[evm2] += 1
                    if len(queue[evm2]) > max_len_queue[evm2]:
                        max_len_queue[evm2] = len(queue[evm2])
                # ЭВМ не занята
                elif temp_n < self.n:
                    t11 = self.choose_t(evm2)
                    f.write("\nВремя обработки задания A: " + str(t11))
                    temp_n += 1
                    done_exs[evm2][1] += 1
                    done_exs[evm2][0] += 1
                    time[evm2] += t11
                    res[evm2] = res_t_interval + t1 + t11
                    t1 += t11
            f.write("\nВыполнено заданий после текущей итерации: " + str(temp_n))
            f.write("\nОчереди на ЭВМ: " + str(queue[0]) + ' ' + str(queue[1]) + ' ' + str(queue[2]))
        res_t_interval += max(t1, t2[0], t2[1], t2[2])
        # Время простоя
        t_prost = [0, 0, 0]
        t_prost[0] = res_t_interval - time[0]
        t_prost[1] = res_t_interval - time[1]
        t_prost[2] = res_t_interval - time[2]

        # Среднее время в очереди
        sred_t_in_queue[0] /= all_in_queue[0]
        sred_t_in_queue[1] /= all_in_queue[1]
        sred_t_in_queue[2] /= all_in_queue[2]

        f.write("\n\n\nОбщее время работы: " + str(res_t_interval) + " минут")

        f.close()
        return temp_n, res_t_interval, time, done_exs, [len(queue[0]), len(queue[1]), len(
            queue[2])], max_len_queue, all_in_queue, t_prost, sred_t_in_queue

    # Больше одного повторения
    def n_start(self, kol):
        sred_time = [0, 0, 0] # Среднее время работы
        sred_res_t_interval = 0 # Среднее время выполнения поступившего числа заказов
        sred_done_exs = [0, [0, 0], [0, 0]]
        sred_t_prost = [0, 0, 0]
        sred_sred_t_in_queue = [0, 0, 0]
        sred_len_queue = [0, 0, 0]
        for i in range(kol):
            temp_n, res_t_interval, time, done_exs, len_queue, max_len_queue, all_in_queue, t_prost, sred_t_in_queue = self.model()
            sred_res_t_interval += res_t_interval
            for j in [0, 1, 2]:
                sred_time[j] += time[j]
                sred_t_prost[j] += t_prost[j]
                sred_sred_t_in_queue[j] += sred_t_in_queue[j]
                sred_len_queue[j] += len_queue[j]
                if j != 0:
                    sred_done_exs[j][0] += done_exs[j][0]
                    sred_done_exs[j][1] += done_exs[j][1]
                else:
                    sred_done_exs[j] += done_exs[j]
        for j in [0, 1, 2]:
            sred_time[j] /= kol
            sred_t_prost[j] /= kol
            sred_sred_t_in_queue[j] /= kol
            sred_len_queue[j] /= kol
            if j != 0:
                sred_done_exs[j][0] /= kol
                sred_done_exs[j][1] /= kol
            else:
                sred_done_exs[j] /= kol

        return sred_res_t_interval / self.kol, sred_time, sred_done_exs, sred_t_prost, sred_sred_t_in_queue, sred_len_queue

def make_window1():
    layout = [
        [sg.Text("Количество заданий:"), sg.InputText(key="count_task")],
        [sg.Text("Количество повторений:"), sg.InputText(key="count_repeat")],
        [sg.Text("Интервал между заданиями :"), sg.InputText(key="interval_between_task"), sg.Text("+-"),
         sg.InputText(key="interval_between_task_range")],
        [sg.Text("Время обработки:")],
        [sg.Text("T1 :"), sg.InputText(key="time_T1"), sg.Text("+-"), sg.InputText(key="time_T1_range")],
        [sg.Text("T2 :"), sg.InputText(key="time_T2"), sg.Text("+-"), sg.InputText(key="time_T2_range")],
        [sg.Text("T3 :"), sg.InputText(key="time_T3"), sg.Text("+-"), sg.InputText(key="time_T3_range")],
        [sg.Text("Вероятность поступления задания:")],
        [sg.Text("P1 :"), sg.InputText(key="probability_P1")],
        [sg.Text("P2 :"), sg.InputText(key="probability_P2")],
        [sg.Text("P3 :"), sg.InputText(key="probability_P3")],
        [sg.Text("Вероятность поступления задания после обработки первой ЭВМ:")],
        [sg.Text("P2 :"), sg.InputText(key="probability_P2_after")],
        [sg.Text("P3 :"), sg.InputText(key="probability_P3_after")],
        [sg.Button('Выполнить'), sg.Button('Условие'), sg.Button('Очистить'), sg.Button('Выход')]
    ]

    return sg.Window('Лабораторная работа 6', layout, finalize=True).Finalize()

def make_window2(model, kol, kol_task):
    layout = []
    if int(kol) > 1:
        res_t_interval, time, done_exs, t_prost, sred_t_in_queue, len_queue = model.n_start(int(kol))
        # time[0] *= int(kol)
        # time[1] *= int(kol)
        # time[2] *= int(kol)
        layout = [[sg.Text(f'Выполнено заданий:{kol_task}')],
                  [sg.Text(f'Количество повторений:{kol}')],
                  [sg.Text(f'Среднее время работы над заданиями:{round(res_t_interval, 4)} м.')],
                  [sg.Text(f'ЭВМ 1:Среднее время работы над заданиями:{round(time[0], 4)} м., '),
                   sg.Text(f'Время простоя:{round(t_prost[0], 4)} м., '), sg.Text(f'Коэффициент использования:{round(time[0] / res_t_interval, 4)}')],
                  [sg.Text(f'ЭВМ 2:Среднее время работы над заданиями:{round(time[1], 4)} м., '),
                   sg.Text(f'Время простоя:{round(t_prost[1], 4)} м., '), sg.Text(f'Коэффициент использования:{round(time[1] / res_t_interval, 4)}')],
                  [sg.Text(f'ЭВМ 3:Среднее время работы над заданиями:{round(time[2], 4)} м., '),
                   sg.Text(f'Время простоя:{round(t_prost[2], 4)} м., '), sg.Text(f'Коэффициент использования:{round(time[2] / res_t_interval, 4)}')],
                  [sg.Text(f'ЭВМ 1:В среднем обработано заданий:{done_exs[0]}, ')],
                  [sg.Text(f'ЭВМ 2:В среднем обработано заданий:{done_exs[1][0]}, '),
                   sg.Text(f'В среднем обработано заданий после ЭВМ 1:{done_exs[1][1]}')],
                  [sg.Text(f'ЭВМ 3:В среднем обработано заданий:{done_exs[2][0]}, '),
                   sg.Text(f'В среднем обработано заданий после ЭВМ 1:{done_exs[2][1]}')],
                  [sg.Text(f'ЭВМ 1:В среднем осталось в очереди:{len_queue[0]}, '),
                   sg.Text(f'Среднее время в очереди:{round(sred_t_in_queue[0],4)} м.')],
                  [sg.Text(f'ЭВМ 2:В среднем осталось в очереди:{len_queue[1]}, '),
                   sg.Text(f'Среднее время в очереди:{round(sred_t_in_queue[1],4)} м.')],
                  [sg.Text(f'ЭВМ 3:В среднем осталось в очереди:{len_queue[2]}, '),
                   sg.Text(f'Среднее время в очереди:{round(sred_t_in_queue[2],4)} м.')],
                  [sg.Button('Вернуться на главную'), sg.Button('Выход')]]
    if int(kol) == 1:
        temp_n, res_t_interval, time, done_exs, len_queue, max_len_queue, all_in_queue, t_prost, sred_t_in_queue = model.model()
        layout = [[sg.Text(f'Выполнено заданий:{kol_task}')],
                  [sg.Text(f'Время работы над заданиями:{round(res_t_interval, 4)} м.')],
                  [sg.Text(f'ЭВМ 1:Время работы над заданиями:{round(time[0], 4)} м., '),
                   sg.Text(f'Время простоя:{round(t_prost[0], 4)} м., '),
                   sg.Text(f'Коэффициент использования:{round(time[0] / res_t_interval, 4)}')],
                  [sg.Text(f'ЭВМ 2:Время работы над заданиями:{round(time[1], 4)} м., '),
                   sg.Text(f'Время простоя:{round(t_prost[1], 4)} м., '),
                   sg.Text(f'Коэффициент использования:{round(time[1] / res_t_interval, 4)}')],
                  [sg.Text(f'ЭВМ 3:Время работы над заданиями:{round(time[2], 4)} м., '),
                   sg.Text(f'Время простоя:{round(t_prost[2], 4)} м., '),
                   sg.Text(f'Коэффициент использования:{round(time[2] / res_t_interval, 4)}')],
                  [sg.Text(f'ЭВМ 1:Обработано заданий:{done_exs[0]}, ')],
                  [sg.Text(f'ЭВМ 2:Обработано заданий:{done_exs[1][0]}, '),
                   sg.Text(f'Обработано заданий после ЭВМ 1:{done_exs[1][1]}')],
                  [sg.Text(f'ЭВМ 3:Обработано заданий:{done_exs[2][0]}, '),
                   sg.Text(f'Обработано заданий после ЭВМ 1:{done_exs[2][1]}')],
                  [sg.Text(f'ЭВМ 1:Осталось в очереди:{len_queue[0]}, '),
                   sg.Text(f'Среднее время в очереди:{round(sred_t_in_queue[0], 4)} м.')],
                  [sg.Text(f'ЭВМ 2:Осталось в очереди:{len_queue[1]}, '),
                   sg.Text(f'Среднее время в очереди:{round(sred_t_in_queue[1], 4)} м.')],
                  [sg.Text(f'ЭВМ 3:Осталось в очереди:{len_queue[2]}, '),
                   sg.Text(f'Среднее время в очереди:{round(sred_t_in_queue[2], 4)} м.')],
                  [sg.Button('Вернуться на главную'), sg.Button('Выход')]]

    return sg.Window('Результат', layout, finalize=True).Finalize()

def main():
    window1 = make_window1()
    window2 = None
    while True:
        window, event, values = sg.read_all_windows()
        if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
            break

        if window == window1 and event == "Выход":
            break
        if event == "Очистить":
            window.Element('count_task').update('')
            window.Element('count_repeat').update('')
            window.Element('interval_between_task').update('')
            window.Element('interval_between_task_range').update('')
            window.Element('time_T1').update('')
            window.Element('time_T1_range').update('')
            window.Element('time_T2').update('')
            window.Element('time_T2_range').update('')
            window.Element('time_T3').update('')
            window.Element('time_T3_range').update('')
            window.Element('probability_P1').update('')
            window.Element('probability_P2').update('')
            window.Element('probability_P3').update('')
            window.Element('probability_P2_after').update('')
            window.Element('probability_P3_after').update('')
        if event == "Условие":
            window.Element('count_task').update('200')
            window.Element('count_repeat').update('1')
            window.Element('interval_between_task').update('3')
            window.Element('interval_between_task_range').update('1')
            window.Element('time_T1').update('4')
            window.Element('time_T1_range').update('1')
            window.Element('time_T2').update('3')
            window.Element('time_T2_range').update('1')
            window.Element('time_T3').update('5')
            window.Element('time_T3_range').update('2')
            window.Element('probability_P1').update('0.4')
            window.Element('probability_P2').update('0.3')
            window.Element('probability_P3').update('0.3')
            window.Element('probability_P2_after').update('0.3')
            window.Element('probability_P3_after').update('0.7')
        if event == "Выполнить" and window == window1:
            # Создаем объект класса
            m = Model_lab6(values['count_repeat'],
                           values['count_task'],
                           values['time_T1'], values['time_T1_range'],
                           values['time_T2'], values['time_T2_range'],
                           values['time_T3'], values['time_T3_range'],
                           values['probability_P1'], values['probability_P2'], values['probability_P3'],
                           values['probability_P2_after'],
                           values['probability_P3_after'],
                           values['interval_between_task'], values['interval_between_task_range'])

            window2 = make_window2(m,values['count_repeat'], values['count_task'])
        if window == window2 and event in (sg.WIN_CLOSED, 'Выход'):
            break
        if window == window2 and event == "Вернуться на главную":
            window2.close()
    window1.close()

if __name__ == '__main__':
    main()
    # window = wx.App() # Создание экземпляра нашей программы
    # InputWindow(None) # Вызывается главное меню
    # window.MainLoop() # Основной цикл событий графического интерфейса пользователя
