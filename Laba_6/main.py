import random
import numpy as np
# task_goal = 200
# время до завершения процесса
processes = {'to_new_task': 0.0,    'T1': 0.0,    'T2': 0.0,    'T3': 0.0}
prostoy = {'T1': 0.0,    'T2': 0.0,    'T3': 0.0}
# очереди заданий у машин
work_queue = {'T1': [],   'T2': [],    'T3': [],}
# вероятности распределения новых заданий
task_chances = {'T1': 0.4,    'T2': 0.3,    'T3': 0.3}
# время ожидания
range_between_tasks = {'new_task': (2.0, 4.0),    'T1': (3.0, 5.0), 'T2': (2.0, 4.0),  'T3': (3.0, 7.0)}
# вероятности распределения заданий после Т1
after_T1 = {'T2': 0.3,    'T3': 0.7}
solve_after_T1 = {'T2': 0,'T3': 0}
solved_on = { 'T1': {'new_task': 0},'T2': {'new_task': 0, 'T1': 0}, 'T3': {'new_task': 0, 'T1': 0}}
solved_tasks_count = {'T1': 0, 'T2': 0, 'T3': 0}

# для всех процессов проходит time времени
def pass_time(time):  # time - время которое нужжно пе-ремотать
    values = []
    for process_time in processes.values():
        if process_time > time:
            values.append(float(process_time - time))
        else:  values.append(0.0)
    return dict(zip(processes.keys(), values))
# описание времени выполнения процессов
def get_task():
    return np.random.uniform(*(range_between_tasks['new_task']))
def solve_on_T1():
    return np.random.uniform(*(range_between_tasks['T1']))
def solve_on_T2():
    return np.random.uniform(*(range_between_tasks['T2']))
def solve_on_T3():
    return np.random.uniform(*(range_between_tasks['T3']))

# доступ к данным о процессе через имя машины
solve = {'T1': solve_on_T1, 'T2': solve_on_T2, 'T3': solve_on_T3}

# выбор машины для обработки нового задания
def select_task_chances():
    machine = random.choices(list(task_chances.keys()), list(task_chances.values()))[0]
    return machine

# выбор машины для обработки задания после Т1
def select_after_T1():
    machine = random.choices(list(after_T1.keys()), list(after_T1.values()))[0]
    return machine

# задание на обработку для machine. запускает её либо увеличивает очередь
def solve_on(machine, source):
    if len(work_queue[machine]) > 0 or processes[machine] > 0.0:
        work_queue[machine].append(source)
    else:
        processes[machine] = solve[machine]()
        solved_on[machine][source] -= -1

# помещает задание из очереди machine на выполнение, если очередь не пустая
def solve_next(machine):
    if len(work_queue[machine]) > 0:
        solved_on[machine][work_queue[machine].pop(0)] += 1
        processes[machine] = solve[machine]()
        # передача задания дальше после данных процессов

def task_came():
    next = select_task_chances()
    solve_on(next, 'new_task')

def solved_on_T1():
    solved_tasks_count['T1'] -= -1
    next = select_after_T1()
    solve_after_T1[next] += 1
    solve_on(next, 'T1')

def simulate():
    overall_time = get_task()
    completed_tasks = 0
    time_without_work = overall_time
    for proc in prostoy.keys():
        prostoy[proc] += overall_time
    task_came()
    global processes
    processes['to_new_task'] += get_task()
    while completed_tasks < task_goal:
        # находим процесс, который завершится раньше других
        working_processes = dict(filter(lambda item: item[1] > 0.0, processes.items()))
        nearest_process = min(working_processes, key=processes.get)
        # проматываем время до его выполнения
        overall_time += processes[nearest_process]
        if len(working_processes) == 1:
            time_without_work += processes[nearest_process]
        for proc in prostoy.keys():
            if proc not in working_processes.keys():
                prostoy[proc] += processes[nearest_process]
        processes = pass_time(processes[nearest_process])
        processes[nearest_process] = 0.0
        match nearest_process:
            case 'to_new_task':  # если пришло новое задание отправляем на выполнение
                task_came()  # и ждём следующее
                processes['to_new_task'] = get_task()
            case 'T1':  # если отработала Т1 отправляем на отстальные машины
                solved_on_T1()
            case 'T2':  # если отработала Т2 отправляем на Т3
                completed_tasks += 1
                solved_tasks_count['T2'] += 1
            case 'T3':  # если отработала Т3 задание выполнено
                completed_tasks += 1
                solved_tasks_count['T3'] += 1
        if nearest_process in solve.keys():  # если машина закончила выполнение
            solve_next(nearest_process)  # она проверяет очередь заданий
    return overall_time, time_without_work, prostoy

input = open('data.txt', 'r').read()
d = input.split('\n')
input_data = []

for string in d:
    input_data += list(map(float, string.split(' ')))
task_goal = int(input_data[0])
task_chances['T1'] = input_data[1]
task_chances['T2'] = input_data[2]
task_chances['T3'] = input_data[3]
after_T1['T2'] = input_data[4]
after_T1['T3'] = input_data[5]
range_between_tasks['new_task'] = (input_data[6] - input_data[7], input_data[6] + input_data[7])
range_between_tasks['T1'] = (input_data[8] - input_data[9], input_data[8] + input_data[9])
range_between_tasks['T2'] = (input_data[10] - input_data[11], input_data[10] + input_data[11])
range_between_tasks['T3'] = (input_data[12] - input_data[13], input_data[12] + input_data[13])

def replay_programm(count_replay):
    res_passages = [0, 0, 0, 0]
    overall_time_passages, absolute_throughput, relative_throughput, load_factor = 0, 0, 0, 0
    for i in range(count_replay):
        one_passage = simulate()
        overall_time_passages += one_passage[0]
        absolute_throughput += task_goal / one_passage[0]
        relative_throughput += task_goal / (task_goal + sum(list(map(len, work_queue.values()))))
        load_factor += one_passage[1] / one_passage[0]
    res_passages[0] = overall_time_passages/count_replay
    res_passages[1] = absolute_throughput/count_replay
    res_passages[2] = relative_throughput/count_replay
    res_passages[3] = load_factor/count_replay
    return res_passages
result = simulate()
print("Коэффициент загрузки каждой машины:" + "\n"
      "\tT1: " + str(round((result[0] - result[2]['T1']) / result[0], 3)) + "\n"
      "\tT2: " + str(round((result[0] - result[2]['T2']) / result[0], 3)) + "\n"
      "\tT3: " + str(round((result[0] - result[2]['T3']) / result[0], 3)))
print("Время работы каждой машины:" + "\n"
      "\tT1: " + str(round((result[0] - result[2]['T1']), 2)) + "\n"
      "\tT2: " + str(round((result[0] - result[2]['T2']), 2)) + "\n"
      "\tT3: " + str(round((result[0] - result[2]['T3']), 2)))
print("Очередь задач на каждой из машин: " +
      "\n\tT1: " + str(int(len(work_queue['T1']))) +
      "\n\tT2: " + str(int(len(work_queue['T2']))) +
      "\n\tT3: " + str(int(len(work_queue['T3']))))
print("Количество выполненных задач: "
      "\n\tT1: " + str(int(solved_tasks_count['T1'])) +
      "\n\tT2: " + str(int(solved_tasks_count['T2'])) +
      "\n\tT3: " + str(int(solved_tasks_count['T3'])))
print("Количество задач идущиx на машину T2: "
      "\n\tновые задачи: " + str(int(solved_on['T2']['new_task'])) +
      "\n\tзадач с T1: " + str(int(solved_on['T2']['T1'])))
print("Количество задач идущиx на машину T3: "
      "\n\tновые задачи: " + str(int(solved_on['T3']['new_task'])) +
      "\n\tзадач с T1: " + str(int(solved_on['T3']['T1'])))
result_replay_passages = replay_programm(1)
print("Время работы программы в среднем: " + str(int(result_replay_passages[0])))
print("Абсолютная пропусная способность в среднем: " + str(round(result_replay_passages[1], 3)))
print("Относительная пропусная способность в среднем: " + str(round(result_replay_passages[2], 3)))
print("Коэффициент загрузки в среднем: " + str(round(1 - result_replay_passages[3], 3)))



