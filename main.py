singleElement = list()
tasks = dict()  # contains all the tasks
branches = list()
subset = dict()


def read_task():
    global singleElement, tasks
    file = open('cpm.txt')  # TWO FILES: cpm.txt and cpm1.txt
    for line in file:  # slide the file line by line
        singleElement = (line.split(','))  # split a line in sub parts
        if 'input' in singleElement[0]:
            tasks['task_' + str(singleElement[0])] = dict()
            tasks['task_' + str(singleElement[0])]['name'] = singleElement[0]
            tasks['task_' + str(singleElement[0])]['value'] = int(singleElement[1])
            tasks['task_' + str(singleElement[0])]['isCritical'] = False
            tasks['task_' + str(singleElement[0])]['branch'] = False
            tasks['task_' + str(singleElement[0])]['subset'] = list()
        if 'sub' in singleElement[0]:
            subset[str(singleElement[1])] = list()
            for i in range(2, len(singleElement)):
                if str(singleElement[i]) == '\n' or str(singleElement[i]) == '':
                    break
                subset[str(singleElement[1])].append(str(singleElement[i]))


def AND(a, b):
    if a == 1 and b == 1:
        return 1
    else:
        return 0


def NAND(a, b):
    if a == 1 and b == 1:
        return 0
    else:
        return 1


def OR(a, b):
    if a == 1 or b == 1:
        return 1
    else:
        return 0


def XOR(a, b):
    if a != b:
        return 1
    else:
        return 0


def NOT(a):
    if not a:
        return 1
    return 0


def NOR(a, b):
    if(a == 0) and (b == 0):
        return 1
    elif(a == 0) and (b == 1):
        return 0
    elif(a == 1) and (b == 0):
        return 0
    elif(a == 1) and (b == 1):
        return 0


def critical_path(value, name_gates, gates, input_1, input_2, task_1, task_2):

    tasks['task_' + str(name_gates)] = dict()
    tasks['task_' + str(name_gates)]['name'] = name_gates
    tasks['task_' + str(name_gates)]['value'] = value
    tasks['task_' + str(name_gates)]['isCritical'] = False
    tasks['task_' + str(name_gates)]['branch'] = False
    tasks['task_' + str(name_gates)]['subset'] = list()
    if task_2 in branches:
        # print(tasks['task_' + task_2]['name'])
        tasks['task_' + task_2]['branch'] = True
        try:
            # print(subset[task_2])
            for i in subset[task_2]:
                tasks['task_' + i]['isCritical'] = False
        except:
            pass
    if task_1 in branches:
        tasks['task_' + task_1]['branch'] = True
        # print(tasks['task_' + task_1]['name'])
        try:
            # print(subset[task_2])
            for i in subset[task_1]:
                tasks['task_' + i]['isCritical'] = False
        except:
            pass

    branches.append(task_1)
    branches.append(task_2)
    if gates == 'NAND':
        if input_1 == 1 and input_2 == 1:
            tasks['task_'+task_1]['isCritical'] = True
            tasks['task_'+task_2]['isCritical'] = True
        if input_1 == 1 and input_2 == 0:
            tasks['task_'+task_2]['isCritical'] = True
        if input_1 == 0 and input_2 == 1:
            tasks['task_'+task_1]['isCritical'] = True

    if gates == 'AND':
        pass

    if gates == 'XOR':
        pass

    if gates == 'OR':
        pass

    if gates == 'NOT':
        pass
    # print('critical ', value, name_gates, gates, input_1, input_2, task_1, task_2, branches)


def c17():
    read_task()
    n10 = NAND(tasks['task_input_1']['value'], tasks['task_input_3']['value'])
    critical_path(
        n10, 'n10', 'NAND', tasks['task_input_1']['value'], tasks['task_input_3']['value'],
        tasks['task_input_1']['name'], tasks['task_input_3']['name']
    )
    n11 = NAND(tasks['task_input_3']['value'], tasks['task_input_6']['value'])
    critical_path(
        n11, 'n11', 'NAND', tasks['task_input_3']['value'], tasks['task_input_6']['value'],
        tasks['task_input_3']['name'], tasks['task_input_6']['name']
    )
    n16 = NAND(tasks['task_input_2']['value'], n11)
    critical_path(
        n16, 'n16', 'NAND', tasks['task_input_2']['value'], tasks['task_n11']['value'],
        tasks['task_input_2']['name'], tasks['task_n11']['name']
    )
    n19 = NAND(n11, tasks['task_input_7']['value'])
    critical_path(
        n19, 'n19', 'NAND', tasks['task_n11']['value'], tasks['task_input_7']['value'],
        tasks['task_n11']['name'], tasks['task_input_7']['name']
    )
    n22 = NAND(n10, n16)
    critical_path(
        n22, 'n22', 'NAND', tasks['task_n10']['value'], tasks['task_n16']['value'],
        tasks['task_n10']['name'], tasks['task_n16']['name']
    )
    n23 = NAND(n16, n19)
    critical_path(
        n23, 'n23', 'NAND', tasks['task_n16']['value'], tasks['task_n19']['value'],
        tasks['task_n16']['name'], tasks['task_n19']['name']
    )
    # print(f'n10 : {n10}, n11 : {n11}, n16: {n16}, n19: {n19} ,n22: {n22} ,n23: {n23}')


c17()
# =============================================================================
# PRINTING
# =============================================================================


for task in tasks:
    if str(tasks[task]['isCritical']) == 'True':
        # print(str(tasks[task]['name']) + ', ' + str(tasks[task]['value']) + ', ' + str(tasks[task]['isCritical']) +
        # ', ' + str(tasks[task]['branch']))
        print(f"stuck at {tasks[task]['value']} in {tasks[task]['name']}")


