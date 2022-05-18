import wx  # Импортируем пакет для работы с wxPython.
import random
import PySimpleGUI as sg

class Model_lab6:
    def __init__(self, kol, n, t1, t1_r, t2, t2_r, t3, t3_r, p1, p2, p3, p1_2, p1_3, interv, interv_r):
        self.kol = int(kol)
        self.n = int(n)
        self.t1 = float(t1)
        self.t1_range = float(t1_r)
        self.t2 = float(t2)
        self.t2_range = float(t2_r)
        self.t3 = float(t3)
        self.t3_range = float(t3_r)
        self.p1 = float(p1)
        self.p2 = float(p2)
        self.p3 = float(p3)
        self.p1_2 = float(p1_2)
        self.p1_3 = float(p1_3)
        self.interv = float(interv)
        self.interv_range = float(interv_r)

    def choose_t(self, evm):
        if evm == 0:
            return random.uniform(self.t1 - self.t1_range, self.t1 + self.t1_range)
        elif evm == 1:
            return random.uniform(self.t2 - self.t2_range, self.t2 + self.t2_range)
        elif evm == 2:
            return random.uniform(self.t3 - self.t3_range, self.t3 + self.t3_range)

    def model(self):
        f = open('result.txt', 'w')
        res_t_interval = 0
        res = [0, 0, 0]
        done_exs = [0, [0, 0], [0, 0]]
        queue = [[], [], []]
        temp_n = 0
        time = [0, 0, 0]
        interval = 0
        tt = 0
        max_len_queue = [0, 0, 0]
        all_in_queue = [0, 0, 0]
        sred_t_in_queue = [0, 0, 0]
        while temp_n < self.n:
            t1 = 0
            t2 = [0, 0, 0]
            t21 = 0
            t11 = 0
            if temp_n > 0:
                interval = random.uniform(self.interv - self.interv_range, self.interv + self.interv_range)
            res_t_interval += interval
            evm = random.choices([0, 1, 2], weights=[self.p1, self.p2, self.p3])[0]
            f.write("\n\n\nЗадание на ЭВМ " + str(evm + 1))
            f.write("\nИнтервал до этого задания (интенсивность): " + str(interval))
            to_queue = False
            if res[evm] > res_t_interval or queue[evm] != []:
                queue[evm].append((1, res_t_interval))
                f.write("\nВ очередь")
                to_queue = True
                all_in_queue[evm] += 1
                if len(queue[evm]) > max_len_queue[evm]:
                    max_len_queue[evm] = len(queue[evm])
            else:
                t1 = self.choose_t(evm)
                f.write("\nИнтервал времени обработки задания: " + str(t1))
                time[evm] += t1
                if evm == 0:
                    done_exs[evm] += 1
                else:
                    done_exs[evm][0] += 1
                    temp_n += 1
                f.write("\nНе из очереди")
                res[evm] = res_t_interval + t1
            for i in [0, 1, 2]:
                if temp_n < self.n and queue[i] != [] and res[i] < res_t_interval:
                    t2[i] = self.choose_t(i)
                    f.write("\nИнтервал времени обработки задания, которое выполняется параллельно на " + str(
                        i + 1) + ": " + str(t2[i]))
                    time[i] += t2[i]
                    res[i] += t2[i]
                    if queue[i][0][0] == 2:
                        done_exs[i][1] += 1
                    sred_t_in_queue[i] += res_t_interval - queue[i][0][1]
                    del (queue[i][0])
                    if i != 0:
                        done_exs[i][0] += 1
                        temp_n += 1
                    else:
                        done_exs[i] += 1
                        evm2_p = random.choices([1, 2], weights=[self.p1_2, self.p1_3])[0]
                        f.write("\nПродолжаем работать параллельно над заданием на " + str(evm2_p + 1))

                        if res[evm2_p] > res_t_interval - interval + t1:
                            f.write("\nВ очередь")
                            queue[evm2_p].append((2, res_t_interval))
                            all_in_queue[evm2_p] += 1
                            if len(queue[evm2_p]) > max_len_queue[evm2_p]:
                                max_len_queue[evm2_p] = len(queue[evm2_p])
                        else:
                            t21 = self.choose_t(evm2_p)
                            f.write("\nНе в очередь, интервал времени обработки задания: " + str(t21))
                            done_exs[evm2_p][1] += 1
                            done_exs[evm2_p][0] += 1
                            time[evm2_p] += t21
                            res[evm2_p] = res_t_interval - interval + t2[i] + t21
                            temp_n += 1
                            t2[i] += t21
            if evm == 0 and to_queue == False:
                evm2 = random.choices([1, 2], weights=[self.p1_2, self.p1_3])[0]
                f.write("\nПродолжаем работать над текущим заданием на " + str(evm2 + 1))
                if res[evm2] > res_t_interval + t1:
                    f.write("\nВ очередь")
                    queue[evm2].append((2, res_t_interval))
                    all_in_queue[evm2] += 1
                    if len(queue[evm2]) > max_len_queue[evm2]:
                        max_len_queue[evm2] = len(queue[evm2])
                elif temp_n < self.n:
                    t11 = self.choose_t(evm2)
                    f.write("\nНе в очередь, интервал времени обработки задания: " + str(t11))
                    temp_n += 1
                    done_exs[evm2][1] += 1
                    done_exs[evm2][0] += 1
                    time[evm2] += t11
                    res[evm2] = res_t_interval + t1 + t11
                    t1 += t11
            f.write("\nВыполнено заданий после этого шага: " + str(temp_n))
            f.write("\nОчереди после этого шага: " + str(queue[0]) + ' ' + str(queue[1]) + ' ' + str(queue[2]))
        res_t_interval += max(t1, t2[0], t2[1], t2[2])
        t_prost = [0, 0, 0]
        t_prost[0] = res_t_interval - time[0]
        t_prost[1] = res_t_interval - time[1]
        t_prost[2] = res_t_interval - time[2]
        sred_t_in_queue[0] /= all_in_queue[0]
        sred_t_in_queue[1] /= all_in_queue[1]
        sred_t_in_queue[2] /= all_in_queue[2]
        f.write("\n\n\nОбщее время работы: " + str(res_t_interval) + " минут")
        f.close()
        return temp_n, res_t_interval, time, done_exs, [len(queue[0]), len(queue[1]), len(
            queue[2])], max_len_queue, all_in_queue, t_prost, sred_t_in_queue

    def n_start(self):
        sred_time = [0, 0, 0]
        sred_res_t_interval = 0
        sred_done_exs = [0, [0, 0], [0, 0]]
        sred_t_prost = [0, 0, 0]
        sred_sred_t_in_queue = [0, 0, 0]
        sred_len_queue = [0, 0, 0]
        for i in range(self.kol):
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
                sred_time[j] /= self.kol
                sred_t_prost[j] /= self.kol
                sred_sred_t_in_queue[j] /= self.kol
                sred_len_queue[j] /= self.kol
                if j != 0:
                    sred_done_exs[j][0] /= self.kol
                    sred_done_exs[j][1] /= self.kol
                else:
                    sred_done_exs[j] /= self.kol

        return sred_res_t_interval / self.kol, sred_time, sred_done_exs, sred_t_prost, sred_sred_t_in_queue, sred_len_queue




class FirstW(wx.Panel):
    def __init__(self, parent):
        super(FirstW, self).__init__(parent)
        # Ввод количества заданий
        self.text_n = wx.StaticText(self, label="Количество заданий :  ", pos=(50, 15))
        self.n = wx.TextCtrl(self, pos=(180, 15))

        # Ввод интервала между заданиями
        self.text_int = wx.StaticText(self, label="Интервал между заданиями =", pos=(50, 45))
        self.text_int = wx.StaticText(self, label="+-", pos=(275, 45))
        self.int = wx.TextCtrl(self, pos=(220, 40), size=(50, 23))
        self.int_range = wx.TextCtrl(self, pos=(294, 40), size=(50, 23))

        # Ввод времени обработки заданий
        self.text_t = wx.StaticText(self, label="Время обработки заданий:", pos=(50, 75))
        self.text_t1 = wx.StaticText(self, label="Т1 = ", pos=(50, 105))
        self.text_t2 = wx.StaticText(self, label="Т2 = ", pos=(50, 135))
        self.text_t3 = wx.StaticText(self, label="Т3 = ", pos=(50, 165))
        self.text_t1 = wx.StaticText(self, label="+-", pos=(132, 105))
        self.text_t2 = wx.StaticText(self, label="+-", pos=(132, 135))
        self.text_t3 = wx.StaticText(self, label="+-", pos=(132, 165))
        self.t1 = wx.TextCtrl(self, pos=(80, 100), size=(50, 23))
        self.t2 = wx.TextCtrl(self, pos=(80, 130), size=(50, 23))
        self.t3 = wx.TextCtrl(self, pos=(80, 160), size=(50, 23))
        self.t1_range = wx.TextCtrl(self, pos=(150, 100), size=(50, 23))
        self.t2_range = wx.TextCtrl(self, pos=(150, 130), size=(50, 23))
        self.t3_range = wx.TextCtrl(self, pos=(150, 160), size=(50, 23))
        self.text_p = wx.StaticText(self, label="Вероятность попадания заданий на ЭВМ:", pos=(50, 195))
        self.text_p1 = wx.StaticText(self, label="Р1 = ", pos=(50, 225))
        self.text_p2 = wx.StaticText(self, label="Р2 = ", pos=(50, 255))
        self.text_p3 = wx.StaticText(self, label="Р3 = ", pos=(50, 285))
        self.p1 = wx.TextCtrl(self, pos=(80, 220))
        self.p2 = wx.TextCtrl(self, pos=(80, 250))
        self.p3 = wx.TextCtrl(self, pos=(80, 280))
        self.text_p = wx.StaticText(self, label="Вероятность попадания заданий на ЭВМ после обработки на 1 ЭВМ:",
                                    pos=(50, 315))
        self.text_p1_2 = wx.StaticText(self, label="Р2 = ", pos=(50, 345))
        self.text_p1_3 = wx.StaticText(self, label="Р3 = ", pos=(50, 375))
        self.p1_2 = wx.TextCtrl(self, pos=(80, 340))
        self.p1_3 = wx.TextCtrl(self, pos=(80, 370))
        self.text_nn = wx.StaticText(self, label="N = ", pos=(300, 420))
        self.nn = wx.TextCtrl(self, pos=(330, 415))
        ex_button = wx.Button(self, label='Пример', pos=(50, 415), size=(150, 30))
        ex_button.Bind(wx.EVT_BUTTON, self.button_click_ex)
        start_button = wx.Button(self, label='Один запуск', pos=(50, 455), size=(150, 30))
        start_button.Bind(wx.EVT_BUTTON, self.button_click_start)
        start2_button = wx.Button(self, label='N запусков', pos=(300, 455), size=(150, 30))
        start2_button.Bind(wx.EVT_BUTTON, self.button_click_start2)

    def button_click_ex(self, event):
        self.n.SetValue(str(200))
        self.t1.SetValue(str(4))
        self.t1_range.SetValue(str(1))
        self.t2.SetValue(str(3))
        self.t2_range.SetValue(str(1))
        self.t3.SetValue(str(5))
        self.t3_range.SetValue(str(2))
        self.p1.SetValue(str(0.4))
        self.p2.SetValue(str(0.3))
        self.p3.SetValue(str(0.3))
        self.p1_2.SetValue(str(0.3))
        self.p1_3.SetValue(str(0.7))
        self.int.SetValue(str(3))
        self.int_range.SetValue(str(1))

    def button_click_start(self, event):
        m = Model_lab6(0, self.n.GetValue(), self.t1.GetValue(), self.t1_range.GetValue(), self.t2.GetValue(),
                       self.t2_range.GetValue(), self.t3.GetValue(), self.t3_range.GetValue(), self.p1.GetValue(),
                       self.p2.GetValue(), self.p3.GetValue(), self.p1_2.GetValue(),
                       self.p1_3.GetValue(), self.int.GetValue(), self.int_range.GetValue())
        MainWindow2(None, m)

    def button_click_start2(self, event):
        m = Model_lab6(self.nn.GetValue(), self.n.GetValue(), self.t1.GetValue(), self.t1_range.GetValue(),
                       self.t2.GetValue(), self.t2_range.GetValue(),
                       self.t3.GetValue(), self.t3_range.GetValue(), self.p1.GetValue(), self.p2.GetValue(),
                       self.p3.GetValue(), self.p1_2.GetValue(),
                       self.p1_3.GetValue(), self.int.GetValue(), self.int_range.GetValue())
        MainWindow3(None, self.nn.GetValue(), m)


class SecondW(wx.Panel):
    def __init__(self, parent, m):
        super(SecondW, self).__init__(parent)
        temp_n, res_t_interval, time, done_exs, len_queue, max_len_queue, all_in_queue, t_prost, sred_t_in_queue = m.model()

        self.text_n = wx.StaticText(self, label="Выполнено заданий:", pos=(50, 15))
        self.n = wx.TextCtrl(self, pos=(180, 10)).SetValue(str(temp_n))
        self.text_res_time = wx.StaticText(self, label="Общее время работы над заданиями:", pos=(50, 45))
        self.res_time = wx.TextCtrl(self, pos=(280, 40)).SetValue(str(round(res_t_interval, 2)) + ' мин.')
        self.text_time = wx.StaticText(self, label="Время работы над заданиями:", pos=(50, 75))
        self.text_t1 = wx.StaticText(self, label="ЭВМ 1 = ", pos=(50, 105))
        self.text_t2 = wx.StaticText(self, label="ЭВМ 2 = ", pos=(50, 135))
        self.text_t3 = wx.StaticText(self, label="ЭВМ 3 = ", pos=(50, 165))
        self.t1 = wx.TextCtrl(self, pos=(100, 100)).SetValue(str(round(time[0], 2)) + ' мин.')
        self.t2 = wx.TextCtrl(self, pos=(100, 130)).SetValue(str(round(time[1], 2)) + ' мин.')
        self.t3 = wx.TextCtrl(self, pos=(100, 160)).SetValue(str(round(time[2], 2)) + ' мин.')
        self.text_time = wx.StaticText(self, label="Время простоя:", pos=(250, 75))
        self.t1 = wx.TextCtrl(self, pos=(250, 100)).SetValue(str(round(t_prost[0], 2)) + ' мин.')
        self.t2 = wx.TextCtrl(self, pos=(250, 130)).SetValue(str(round(t_prost[1], 2)) + ' мин.')
        self.t3 = wx.TextCtrl(self, pos=(250, 160)).SetValue(str(round(t_prost[2], 2)) + ' мин.')
        self.text_time = wx.StaticText(self, label="Коэффициент использования:", pos=(400, 75))
        self.t1 = wx.TextCtrl(self, pos=(400, 100)).SetValue(str(round(time[0] / res_t_interval, 2)))
        self.t2 = wx.TextCtrl(self, pos=(400, 130)).SetValue(str(round(time[1] / res_t_interval, 2)))
        self.t3 = wx.TextCtrl(self, pos=(400, 160)).SetValue(str(round(time[2] / res_t_interval, 2)))
        self.text_res_kol = wx.StaticText(self, label="Всего обработано заданий:", pos=(50, 195))
        self.text_res_kol1 = wx.StaticText(self, label="ЭВМ 1 = ", pos=(50, 225))
        self.text_res_kol2 = wx.StaticText(self, label="ЭВМ 2 = ", pos=(50, 255))
        self.text_res_kol3 = wx.StaticText(self, label="ЭВМ 3 = ", pos=(50, 285))
        self.res_kol1 = wx.TextCtrl(self, pos=(100, 220)).SetValue(str(done_exs[0]))
        self.res_kol2 = wx.TextCtrl(self, pos=(100, 250)).SetValue(str(done_exs[1][0]))
        self.res_kol3 = wx.TextCtrl(self, pos=(100, 280)).SetValue(str(done_exs[2][0]))
        self.text_res_kol = wx.StaticText(self, label="Обработано заданий после 1:", pos=(250, 225))
        self.res_kol2 = wx.TextCtrl(self, pos=(250, 250)).SetValue(str(done_exs[1][1]))
        self.res_kol3 = wx.TextCtrl(self, pos=(250, 280)).SetValue(str(done_exs[2][1]))
        self.text_queue = wx.StaticText(self, label="Осталось заданий в очереди:", pos=(50, 315))
        self.text_queue1 = wx.StaticText(self, label="ЭВМ 1:", pos=(50, 345))
        self.text_queue2 = wx.StaticText(self, label="ЭВМ 2:", pos=(50, 375))
        self.text_queue3 = wx.StaticText(self, label="ЭВМ 3:", pos=(50, 405))
        self.queue1 = wx.TextCtrl(self, pos=(100, 340)).SetValue(str(len_queue[0]))
        self.queue2 = wx.TextCtrl(self, pos=(100, 370)).SetValue(str(len_queue[1]))
        self.queue3 = wx.TextCtrl(self, pos=(100, 400)).SetValue(str(len_queue[2]))
        self.text_queue = wx.StaticText(self, label="Макс. количество в очереди:", pos=(250, 315))
        self.queue1 = wx.TextCtrl(self, pos=(250, 340)).SetValue(str(max_len_queue[0]))
        self.queue2 = wx.TextCtrl(self, pos=(250, 370)).SetValue(str(max_len_queue[1]))
        self.queue3 = wx.TextCtrl(self, pos=(250, 400)).SetValue(str(max_len_queue[2]))
        self.text_queue = wx.StaticText(self, label="Всего попадало в очередь:", pos=(50, 435))
        self.text_queue1 = wx.StaticText(self, label="ЭВМ 1:", pos=(50, 465))
        self.text_queue2 = wx.StaticText(self, label="ЭВМ 2:", pos=(50, 495))
        self.text_queue3 = wx.StaticText(self, label="ЭВМ 3:", pos=(50, 525))
        self.queue1 = wx.TextCtrl(self, pos=(100, 460)).SetValue(str(all_in_queue[0]))
        self.queue2 = wx.TextCtrl(self, pos=(100, 490)).SetValue(str(all_in_queue[1]))
        self.queue3 = wx.TextCtrl(self, pos=(100, 520)).SetValue(str(all_in_queue[2]))
        self.text_queue = wx.StaticText(self, label="Среднее время в очереди:", pos=(250, 435))
        self.queue1 = wx.TextCtrl(self, pos=(250, 460)).SetValue(str(round(sred_t_in_queue[0], 2)) + ' мин.')
        self.queue2 = wx.TextCtrl(self, pos=(250, 490)).SetValue(str(round(sred_t_in_queue[1], 2)) + ' мин.')
        self.queue3 = wx.TextCtrl(self, pos=(250, 520)).SetValue(str(round(sred_t_in_queue[2], 2)) + ' мин.')


class ThirdW(wx.Panel):
    def __init__(self, parent, kol, m):
        super(ThirdW, self).__init__(parent)
        res_t_interval, time, done_exs, t_prost, sred_t_in_queue, len_queue = m.n_start()
        self.text_n = wx.StaticText(self, label="Выполнено запусков:", pos=(50, 15))
        self.n = wx.TextCtrl(self, pos=(180, 10)).SetValue(str(kol))
        self.text_res_time = wx.StaticText(self, label="Среднее время работы над заданиями:", pos=(50, 45))
        self.res_time = wx.TextCtrl(self, pos=(280, 40)).SetValue(str(round(res_t_interval, 2)) + ' мин.')
        self.text_time = wx.StaticText(self, label="Среднее время работы:", pos=(50, 75))
        self.text_t1 = wx.StaticText(self, label="ЭВМ 1 = ", pos=(50, 105))
        self.text_t2 = wx.StaticText(self, label="ЭВМ 2 = ", pos=(50, 135))
        self.text_t3 = wx.StaticText(self, label="ЭВМ 3 = ", pos=(50, 165))
        self.t1 = wx.TextCtrl(self, pos=(100, 100)).SetValue(str(round(time[0], 2)) + ' мин.')
        self.t2 = wx.TextCtrl(self, pos=(100, 130)).SetValue(str(round(time[1], 2)) + ' мин.')
        self.t3 = wx.TextCtrl(self, pos=(100, 160)).SetValue(str(round(time[2], 2)) + ' мин.')
        self.text_time = wx.StaticText(self, label="Среднее время простоя:", pos=(250, 75))
        self.t1 = wx.TextCtrl(self, pos=(250, 100)).SetValue(str(round(t_prost[0], 2)) + ' мин.')
        self.t2 = wx.TextCtrl(self, pos=(250, 130)).SetValue(str(round(t_prost[1], 2)) + ' мин.')
        self.t3 = wx.TextCtrl(self, pos=(250, 160)).SetValue(str(round(t_prost[2], 2)) + ' мин.')
        self.text_time = wx.StaticText(self, label="Коэффициент использования:", pos=(400, 75))
        self.t1 = wx.TextCtrl(self, pos=(400, 100)).SetValue(str(round(time[0] / res_t_interval, 2)))
        self.t2 = wx.TextCtrl(self, pos=(400, 130)).SetValue(str(round(time[1] / res_t_interval, 2)))
        self.t3 = wx.TextCtrl(self, pos=(400, 160)).SetValue(str(round(time[2] / res_t_interval, 2)))
        self.text_res_kol = wx.StaticText(self, label="В среднем обработано заданий:", pos=(50, 195))
        self.text_res_kol1 = wx.StaticText(self, label="ЭВМ 1 = ", pos=(50, 225))
        self.text_res_kol2 = wx.StaticText(self, label="ЭВМ 2 = ", pos=(50, 255))
        self.text_res_kol3 = wx.StaticText(self, label="ЭВМ 3 = ", pos=(50, 285))
        self.res_kol1 = wx.TextCtrl(self, pos=(100, 220)).SetValue(str(done_exs[0]))
        self.res_kol2 = wx.TextCtrl(self, pos=(100, 250)).SetValue(str(done_exs[1][0]))
        self.res_kol3 = wx.TextCtrl(self, pos=(100, 280)).SetValue(str(done_exs[2][0]))
        self.text_res_kol = wx.StaticText(self, label="Обработано заданий после 1:", pos=(250, 225))
        self.res_kol2 = wx.TextCtrl(self, pos=(250, 250)).SetValue(str(done_exs[1][1]))
        self.res_kol3 = wx.TextCtrl(self, pos=(250, 280)).SetValue(str(done_exs[2][1]))

        self.text_queue = wx.StaticText(self, label="В среднем осталось в очереди:", pos=(50, 315))
        self.text_queue1 = wx.StaticText(self, label="ЭВМ 1:", pos=(50, 345))
        self.text_queue2 = wx.StaticText(self, label="ЭВМ 2:", pos=(50, 375))
        self.text_queue3 = wx.StaticText(self, label="ЭВМ 3:", pos=(50, 405))
        self.queue1 = wx.TextCtrl(self, pos=(100, 340)).SetValue(str(len_queue[0]))
        self.queue2 = wx.TextCtrl(self, pos=(100, 370)).SetValue(str(len_queue[1]))
        self.queue3 = wx.TextCtrl(self, pos=(100, 400)).SetValue(str(len_queue[2]))
        self.text_queue = wx.StaticText(self, label="Среднее время в очереди:", pos=(250, 315))
        self.queue1 = wx.TextCtrl(self, pos=(250, 340)).SetValue(str(round(sred_t_in_queue[0], 2)) + ' мин.')
        self.queue2 = wx.TextCtrl(self, pos=(250, 370)).SetValue(str(round(sred_t_in_queue[1], 2)) + ' мин.')
        self.queue3 = wx.TextCtrl(self, pos=(250, 400)).SetValue(str(round(sred_t_in_queue[2], 2)) + ' мин.')


# Окно ввода
class InputWindow(wx.Frame):
    def __init__(self, parent):
        super(InputWindow, self).__init__(parent, size=(600, 640)) # Создание окна вывода
        mpnl = FirstW(self)
        self.SetTitle('Ввод данных') # Установка названия
        self.Show(True) # Сделать видимым



class MainWindow2(wx.Frame):
    def __init__(self, parent, model):
        super(MainWindow2, self).__init__(parent, size=(600, 610))
        mpnl = SecondW(self, model)
        self.SetTitle('Результаты')
        self.Centre()
        self.Show(True)


class MainWindow3(wx.Frame):
    def __init__(self, parent, kol, model):
        super(MainWindow3, self).__init__(parent, size=(600, 490))
        mpnl = ThirdW(self, kol, model)
        self.SetTitle('Результаты')
        self.Centre()
        self.Show(True)

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
    res_t_interval, time, done_exs, t_prost, sred_t_in_queue, len_queue = model.n_start()
    layout = [[sg.Text(f'Выполнено заданий:{kol_task}')],
              [sg.Text(f'Количество повторений:{kol}')],
              [sg.Text(f'Среднее время работы над заданиями:{round(res_t_interval, 4)}')],
              [sg.Text(f'ЭВМ 1:Время работы над заданиями:{round(time[0], 4)}, '),
               sg.Text(f'Время простоя:{round(t_prost[0], 4)}, '), sg.Text(f'Коэффициент использования:{round(time[0] / res_t_interval, 4)}')],
              [sg.Text(f'ЭВМ 2:Время работы над заданиями:{round(time[1], 4)}, '),
               sg.Text(f'Время простоя:{round(t_prost[1], 4)}'), sg.Text(f'Коэффициент использования:{round(time[1] / res_t_interval, 4)}')],
              [sg.Text(f'ЭВМ 3:Время работы над заданиями:{round(time[2], 4)}, '),
               sg.Text(f'Время простоя:{round(t_prost[2], 4)}'), sg.Text(f'Коэффициент использования:{round(time[2] / res_t_interval, 4)}')],

              [sg.Text(f'ЭВМ 1:Обработано заданий:{done_exs[0]}, ')],
              [sg.Text(f'ЭВМ 2:Обработано заданий:{done_exs[1][0]}, '),
               sg.Text(f'Обработано заданий после ЭВМ 1:{done_exs[1][1]}')],
              [sg.Text(f'ЭВМ 3:Обработано заданий:{done_exs[1][0]}, '),
               sg.Text(f'Обработано заданий после ЭВМ 1:{done_exs[2][1]}')],
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
