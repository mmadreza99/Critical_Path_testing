import random
import re

tasks = dict()  # contains all the tasks
branches = list()
output = dict()
gates = dict()


def read_task():
    counter = 0
    file = open('c17.txt')  # TWO FILES:
    for line in file:  # slide the file line by line

        if '#' in line or line == '\n':
            continue

        if re.match('INPUT.*$', line):
            singleElement = re.findall(r'\w*\((\d*)\)', line)  # split a line in sub parts
            # print(singleElement)
            tasks['input_' + str(singleElement[0])] = dict()
            tasks['input_' + str(singleElement[0])]['name'] = singleElement[0]
            tasks['input_' + str(singleElement[0])]['value'] = random.randint(0, 1)
            tasks['input_' + str(singleElement[0])]['isCritical'] = False
            tasks['input_' + str(singleElement[0])]['branch'] = False
            tasks['input_' + str(singleElement[0])]['subset'] = list()
        if re.match('OUTPUT.*$', line):
            singleElement = re.findall(r'\w*\((\d*)\)', line)  # split a line in sub parts
            single_value = re.findall(r'\d*', line)  # split a line in sub parts
            output['output' + str(singleElement[0])] = dict()
            output['output' + str(singleElement[0])]['name'] = singleElement[0]
            output['output' + str(singleElement[0])]['value'] = single_value[0]
        if '=' in line:
            input_element = (line.split(' '))
            name_gate = input_element[2].split('(')
            text = line.split('=')
            input_ = re.findall('[0-9]{1,3}', text[1])
            result_ = re.findall('[0-9]{1,3}', text[0])
            tasks['input_' + str(input_element[0])] = dict()
            tasks['input_' + str(input_element[0])]['name'] = input_element[0]
            tasks['input_' + str(input_element[0])]['value'] = 0
            tasks['input_' + str(input_element[0])]['isCritical'] = False
            tasks['input_' + str(input_element[0])]['branch'] = False
            tasks['input_' + str(input_element[0])]['subset'] = list()
            gates['gate_' + str(name_gate[0]) + str(counter)] = dict()
            gates['gate_' + str(name_gate[0]) + str(counter)]['name'] = name_gate[0]
            gates['gate_' + str(name_gate[0]) + str(counter)]['input'] = input_
            gates['gate_' + str(name_gate[0]) + str(counter)]['result'] = result_
            counter += 1


def AND(a, b, d='', c='', e='', f='', g='', h='', i=''):
    if i != '':
        if a and b and d and c and e and f and g and h and i:
            return 1
        else:
            return 0

    if e != '':
        if a and b and d and c and e:
            return 1
        else:
            return 0

    if c != '':
        if a and b and d and c:
            return 1
        else:
            return 0
    if d != '':
        if a and b and d:
            return 1
        else:
            return 0
    if a == 1 and b == 1:
        return 1
    else:
        return 0


def NAND(a, b, d='', c=''):
    # print(a, b, d, c)
    if c != '':
        if a and b and d and c == 1:
            return 0
        else:
            return 1
    if d != '':
        if a and b and d == 1:
            return 0
        else:
            return 1
    if a and b == 1:
        return 0
    else:
        return 1


def OR(a, b, d='', c='', e=''):
    if e != '':
        if a == 1 or b == 1 or d == 1 or c == 1 or e == 1:
            return 1
        else:
            return 0
    if c != '':
        if a == 1 or b == 1 or d == 1 or c == 1:
            return 1
        else:
            return 0
    if d != '':
        if a == 1 or b == 1 or d == 1:
            return 1
        else:
            return 0
    if a == 1 or b == 1:
        return 1
    else:
        return 0


def XOR(a, b):
    return a ^ b


def NOT(a):
    if not a:
        return 1
    return 0


def NOR(a, b):
    if (a == 0) and (b == 0):
        return 1
    elif (a == 0) and (b == 1):
        return 0
    elif (a == 1) and (b == 0):
        return 0
    elif (a == 1) and (b == 1):
        return 0


def update_value(value, name_gate):
    # print(value, name_gate[0])
    input_a = 'input_' + str(name_gate[0])
    tasks[input_a]['value'] = value


def subset_check(gate, sub_a, sub_b):
    # print(gate[0], sub_a, sub_b)
    input_a = 'input_' + str(gate[0])
    tasks[input_a]['subset'].append(sub_a)
    tasks[input_a]['subset'].append(sub_b)


def critical_path(str_gates, input_1, input_2, task_1, task_2):
    if task_2 in branches:
        # print('branch :', tasks['input_' + task_2]['name'])
        tasks['input_' + task_2]['branch'] = True
        try:
            # print('subset :', tasks['input_' + task_2]['subset'])
            for i in tasks['input_' + task_2]['subset']:
                tasks['input_' + i]['isCritical'] = False
        finally:
            pass

    if task_1 in branches:
        tasks['input_' + task_1]['branch'] = True
        # print('branch :', tasks['input_' + task_1]['name'])
        try:
            # print('subset :', tasks['input_' + task_2]['subset'])
            for i in tasks['input_' + task_1]['subset']:
                tasks['input_' + i]['isCritical'] = False
        finally:
            pass

    branches.append(task_1)
    branches.append(task_2)

    if str_gates == 'NAND':
        if input_1 == 1 and input_2 == 1:
            tasks['input_' + task_1]['isCritical'] = True
            tasks['input_' + task_2]['isCritical'] = True
        if input_1 == 1 and input_2 == 0:
            tasks['input_' + task_2]['isCritical'] = True
        if input_1 == 0 and input_2 == 1:
            tasks['input_' + task_1]['isCritical'] = True

    if str_gates == 'AND':
        pass

    if str_gates == 'XOR':
        pass

    if str_gates == 'OR':
        pass

    if str_gates == 'NOT':
        pass

    # print('critical ', str_gates, input_1, input_2, task_1, task_2, branches, subset)


def c17():
    read_task()
    for gate in gates:
        if str(gates[gate]['name']) == 'NAND':
            input_a = 'input_' + str(gates[gate]['input'][0])
            input_b = 'input_' + str(gates[gate]['input'][1])
            value = NAND(tasks[input_a]['value'], tasks[input_b]['value'])
            # print(gate, value)
            subset_check(gates[gate]['result'], tasks[input_a]['name'], tasks[input_b]['name'])
            update_value(value, gates[gate]['result'])
            critical_path(
                gates[gate]['name'], tasks[input_a]['value'], tasks[input_b]['value'],
                tasks[input_a]['name'], tasks[input_b]['name']
            )
        if str(gates[gate]['name']) == 'AND':
            input_a = 'input_' + str(gates[gate]['input'][0])
            input_b = 'input_' + str(gates[gate]['input'][1])
            value = AND(tasks[input_a]['value'], tasks[input_b]['value'])
            # print(gate, value)
            subset_check(gates[gate]['result'], tasks[input_a]['name'], tasks[input_b]['name'])
            update_value(value, gates[gate]['result'])
            critical_path(
                gates[gate]['name'], tasks[input_a]['value'], tasks[input_b]['value'],
                tasks[input_a]['name'], tasks[input_b]['name']
            )


c17()
# =============================================================================
# PRINTING
# =============================================================================
for task in tasks:
    if str(tasks[task]['isCritical']) == 'True':
        print(f"stuck at {NOT(tasks[task]['value'])} in {tasks[task]['name']}")

for out in output:
    print(f"stuck at {NOT(output[out]['value'])} in {output[out]['name']}")
