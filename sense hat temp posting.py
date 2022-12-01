from sense_hat import SenseHat
import time
# import requests
import threading
import os
from datetime import datetime
import psutil
import dweepy

sense = SenseHat()
sense.clear()
count = 1
start_time = time.time()

def get_times():
    date_time = datetime.now()
    date = date_time.strftime("%m/%d/%Y")
    now = date_time.strftime("%H:%M:%S")
    cputime = psutil.cpu_times()[0]
    return date, now, cputime
    
def get_memory():
    pid = os.getpid()
    v_mem_active = round((psutil.virtual_memory()[4] / 1000000), 2)
    v_mem_used = psutil.virtual_memory()[2]
    cpu_percent = psutil.cpu_percent()
    context_switches = psutil.cpu_stats()[0]
    interrupts = psutil.cpu_stats()[1]
    return pid, v_mem_active, v_mem_used, cpu_percent, context_switches, interrupts
    
def get_sensors():
    temp = round((sense.get_temperature() * (9/5) + 32),2)
    pressure = round(sense.get_pressure(), 2)
    compass = sense.get_compass_raw()
    x_axis = round(compass['x'], 2)
    y_axis = round(compass['y'], 2)
    z_axis = round(compass['z'], 2)
    return temp, pressure, x_axis, y_axis, z_axis

def count_threads():
    return threading.active_count()
    
thread_times = threading.Thread(target=get_times())
thread_memory = threading.Thread(target=get_memory())
thread_sensors = threading.Thread(target=get_sensors())
# thread_times.run()
# thread_memory.run()
# thread_sensors.run()
#     
while True:
    times = get_times()
    date = times[0]
    now = times[1]
    cputime = times[2]
    
    memory = get_memory()
    pid = memory[0]
    v_mem_active = memory[1]
    v_mem_used = memory[2]
    cpu_percent = memory[3]
    context_switches = memory[4]
    interrupts = memory[5]
    
    sensors = get_sensors()
    temp = sensors[0]
    pressure = sensors[1]
    x_axis = sensors[2]
    y_axis = sensors[3]
    z_axis = sensors[4]
    
    thread_count = count_threads()
    count += 1
    runtime = (round((time.time() - start_time), 6) * 1000) - 5
    data = {'thread count': thread_count,
            'count': count,
            'date': date,
            'time': now,
            'cpu times': cputime,
            'pid': pid,
            'active virtual memory': v_mem_active,
            'used virtual memory': v_mem_used,
            'cpu percent': cpu_percent,
            'context switches': context_switches,
            'interrupts': interrupts,
            'temp': temp,
            'pressure': pressure,
            'x axis': x_axis,
            'y axis': y_axis,
            'z axis': z_axis,
            'runtime': runtime}
    dweepy.dweet_for('ethans_sense_hat', data)
    time.sleep(1)
    start_time = time.time()
    print("sending", count)
