"""
Input example:

90 60 2 10 0
0 25 7 50
18 32
142 70
156 1

Description:

(N of cylinders) (index of start cylinder) (time to switch cylinder) (time to park) (parking index)
(time moment 1) (cylinder index1) (cylinder index2) (cylinder index3)...
(time moment 2) (cylinder index1) (cylinder index2) (cylinder index3)...
(time moment 2) (cylinder index1) (cylinder index2) (cylinder index3)...
(time moment 2) (cylinder index1) (cylinder index2) (cylinder index3)...
...

Russian description:
(кол-во цилиндров) (индекс начального цилиндра) (время для смены цилиндров) (время для парковки) (парковочный цилиндр)
(время прихода запроса) (индекс цилиндра) (ещё индекс цилиндра) (ещё индекс цилиндра)...
(ещё время прихода запроса) (индекс цилиндра) (ещё индекс цилиндра) (ещё индекс цилиндра)...
(ещё время прихода запроса) (индекс цилиндра) (ещё индекс цилиндра) (ещё индекс цилиндра)...
(ещё время прихода запроса) (индекс цилиндра) (ещё индекс цилиндра) (ещё индекс цилиндра)...
...
"""
from queue import *

global_vars = {
    'n_cylinders': 0,
    'start_index': 0,
    'switch_time': 0,
    'park_time': 0,
    'park_index': 0
}
requests_list = []


def parse_input(string_input):
    lines = str(string_input).splitlines()
    if len(lines) <= 1:
        return False
    
    parameters = lines[0].split()
    if len(parameters) != 5:
        return False
    
    try:
        global_vars['n_cylinders'] = int(parameters[0])
        global_vars['start_index'] = int(parameters[1])
        global_vars['switch_time'] = int(parameters[2])
        global_vars['park_time'] = int(parameters[3])
        global_vars['park_index'] = int(parameters[4])
        
        i = 1
        while i < len(lines):
            new_line_args = lines[i].split()
            if len(new_line_args) < 2:
                break
            requests_list.append([int(number) for number in new_line_args])
            i += 1
    except ValueError:
        return False
    return True


# FCFS - first come, first served
def fcfs():
    n_cylinders = global_vars['n_cylinders']
    current_index = global_vars['start_index']
    switch_time = global_vars['switch_time']
    
    time_counter = 0
    
    local_requests = Queue()
    
    for line in requests_list:
        come_time = line[0]
        for i in range(1, len(line)):
            local_requests.put((come_time, line[i]))
    
    result = ""
    while not local_requests.empty():
        new_request = local_requests.get()
        come_time = new_request[0]
        next_index = new_request[1]
        
        if come_time > time_counter:  # if next request isn't received
            result += "Waiting: " + str(come_time - time_counter) + "\n"
            time_counter = come_time
        
        elapsed_time = switch_time * (abs(current_index - next_index))
        result += "{:d} -> {:d} : {:d}\n".format(current_index, next_index, elapsed_time)
        time_counter += elapsed_time
        current_index = next_index
    
    result += "Elapsed time: {:d}".format(time_counter)
    return result


def do_work():
    inp = open("input.txt").read()
    res = parse_input(inp)
    # print("Input is parsed successfully:", res)
    # print("N of cylinders:", global_vars['n_cylinders'])
    # print("Start cylinder:", global_vars['start_index'])
    # print("Switch time:", global_vars['switch_time'])
    # print("Parking time:", global_vars['park_time'])
    # print("Parking index:", global_vars['park_index'])
    if not res:
        return "fail"
    print("_____FCFS:_____")
    print(fcfs())


do_work()
