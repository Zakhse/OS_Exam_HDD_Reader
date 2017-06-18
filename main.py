"""
Use only do_work() function!

Input example:

90 60 2 10
0 25 7 50
18 32
142 70
156 1

Description:

(N of cylinders) (index of start cylinder) (time to switch cylinder) (time to park)
(time moment 1) (cylinder index1) (cylinder index2) (cylinder index3)...
(time moment 2) (cylinder index1) (cylinder index2) (cylinder index3)...
(time moment 2) (cylinder index1) (cylinder index2) (cylinder index3)...
(time moment 2) (cylinder index1) (cylinder index2) (cylinder index3)...
...

Russian description:
(кол-во цилиндров) (индекс начального цилиндра) (время для смены цилиндров) (время для парковки)
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
}
requests_list = []


def parse_input(string_input):
    lines = str(string_input).splitlines()
    if len(lines) <= 1:
        return False
    
    parameters = lines[0].split()
    if len(parameters) != 4:
        return False
    
    try:
        global_vars['n_cylinders'] = int(parameters[0])
        global_vars['start_index'] = int(parameters[1])
        global_vars['switch_time'] = int(parameters[2])
        global_vars['park_time'] = int(parameters[3])
        
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


# SSTF - short seek time first
def sstf():
    current_index = global_vars['start_index']
    switch_time = global_vars['switch_time']
    time_counter = 0
    local_requests = []
    
    def choose_next():
        chosen_entry = None
        nonlocal time_counter
        nonlocal current_index
        min_difference = global_vars['n_cylinders']
        min_wait_time = None
        for entry in local_requests:
            if entry[0] <= time_counter:
                if abs(entry[1] - current_index) < min_difference:
                    chosen_entry = entry
                    min_difference = abs(entry[1] - current_index)
            elif (min_wait_time is None) or (entry[0] - time_counter < min_wait_time):
                min_wait_time = entry[0] - time_counter
        
        if chosen_entry is not None:
            local_requests.remove(chosen_entry)
        return chosen_entry, min_wait_time
    
    for line in requests_list:
        come_time = line[0]
        for i in range(1, len(line)):
            local_requests.append((come_time, line[i]))
    
    result = ""
    while len(local_requests) != 0:
        new_request, time_to_wait = choose_next()
        if new_request is None:
            result += "Waiting: {:d}\n".format(time_to_wait)
            time_counter += time_to_wait
            new_request, time_to_wait = choose_next()
        
        next_index = new_request[1]
        elapsed_time = switch_time * (abs(current_index - next_index))
        result += "{:d} -> {:d} : {:d}\n".format(current_index, next_index, elapsed_time)
        time_counter += elapsed_time
        current_index = next_index
    
    result += "Elapsed time: {:d}".format(time_counter)
    return result


# SCAN
def scan(right = True):
    n_cylinders = global_vars['n_cylinders']
    current_index = global_vars['start_index']
    switch_time = global_vars['switch_time']
    time_counter = 0
    last_elapsed_time = 0
    prev_index = current_index
    local_requests = []
    
    def choose_next():
        nonlocal current_index
        nonlocal time_counter
        
        for entry in local_requests:
            if entry[1] == current_index and entry[0] <= time_counter:
                return entry
        
        return None
    
    for line in requests_list:
        come_time = line[0]
        for i in range(1, len(line)):
            local_requests.append((come_time, line[i]))
    
    result = ""
    while len(local_requests) != 0:
        sequence = range(current_index, n_cylinders - 1) if right else range(current_index, 0, -1)
        for current_index in sequence:
            new_request = choose_next()
            
            if (new_request is not None) or (current_index == 0) or (current_index == n_cylinders - 1):
                result += "{:d} -> {: d}: {: d}\n".format(prev_index, current_index, last_elapsed_time)
                prev_index = current_index
                last_elapsed_time = 0
                if new_request is not None:
                    local_requests.remove(new_request)
                    if len(local_requests) == 0:
                        break
            
            time_counter += switch_time
            last_elapsed_time += switch_time
        
        current_index = n_cylinders - 1 if right else 0
        right = not right
    
    result += "Elapsed time: {:d}".format(time_counter)
    return result


# С-SCAN
def c_scan(right = True):
    n_cylinders = global_vars['n_cylinders']
    current_index = global_vars['start_index']
    switch_time = global_vars['switch_time']
    park_time = global_vars['park_time']
    time_counter = 0
    last_elapsed_time = 0
    prev_index = current_index
    local_requests = []
    
    def choose_next():
        nonlocal current_index
        nonlocal time_counter
        
        for entry in local_requests:
            if entry[1] == current_index and entry[0] <= time_counter:
                return entry
        
        return None
    
    for line in requests_list:
        come_time = line[0]
        for i in range(1, len(line)):
            local_requests.append((come_time, line[i]))
    
    result = ""
    
    start = 0 if right else  n_cylinders - 1
    end = n_cylinders if right else -1
    step = 1 if right else -1
    should_break = False
    while len(local_requests) != 0:
        sequence = range(current_index, end, step)
        for current_index in sequence:
            new_request = choose_next()
            
            if new_request is not None:
                result += "{:d} -> {: d}: {: d}\n".format(prev_index, current_index, last_elapsed_time)
                prev_index = current_index
                last_elapsed_time = 0
                local_requests.remove(new_request)
                if len(local_requests) == 0:
                    should_break = True
                    break
            
            if current_index != abs(end) - 1:
                time_counter += switch_time
                last_elapsed_time += switch_time
        
        if should_break:
            break
        
        # time from last request to end
        result += "{:d} -> {: d}: {: d}\n".format(prev_index, current_index, last_elapsed_time)
        
        last_elapsed_time = 0
        prev_index = current_index
        current_index = start
        
        # time to park
        result += "{:d} -> {: d}: {: d}\n".format(prev_index, current_index, park_time)
        prev_index = current_index
        right = not right
    
    result += "Elapsed time: {:d}".format(time_counter)
    return result


# USE ONLY THIS FUNCTION!!!
def do_work(string_input):
    # string_input = open("input.txt").read()
    res = parse_input(string_input)
    # print("Input is parsed successfully:", res)
    # print("N of cylinders:", global_vars['n_cylinders'])
    # print("Start cylinder:", global_vars['start_index'])
    # print("Switch time:", global_vars['switch_time'])
    # print("Parking time:", global_vars['park_time'])
    # print("Parking index:", global_vars['park_index'])
    if not res:
        return "fail"
    answer = ""
    answer += "_____FCFS:_____\n"
    answer += fcfs() + "\n"
    
    answer += "\n_____SSTF:_____\n"
    answer += sstf() + "\n"
    
    answer += "\n___SCAN (start to right):___\n"
    answer += scan(True) + "\n"
    
    answer += "\n___SCAN (start to left):___\n"
    answer += scan(False) + "\n"
    
    answer += "\n___C-SCAN (start to right):___\n"
    answer += c_scan(True) + "\n"
    
    answer += "\n___C-SCAN (start to left):___\n"
    answer += c_scan(False) + "\n"
    
    return answer
