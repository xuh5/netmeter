from time import sleep
import psutil as p

"""

last_net_io = p.net_io_counters()
current_net_io = last_net_io

dt = 2.0

while True:
    sleep(dt)

    current_net_io = p.net_io_counters()
    delta_upload = current_net_io.bytes_sent - last_net_io.bytes_sent
    delta_recv = current_net_io.bytes_recv - last_net_io.bytes_recv

    KB_speed_upload = int((delta_upload/1024)/dt)
    KB_speed_recv = int((delta_recv/1024)/dt)

    print("The upload speed is: ",KB_speed_upload)
    print("The download speed is: ",KB_speed_recv)

    last_net_io = current_net_io
"""

"""
This is the track speed function, it will calculate the average download and upload speed in a given time slot
the return value of this function will be the next time input
Note: This function is a one-time version of the function above

last_bytes_recv: The value of bytes received in the last call
last_bytes_sent: The value of bytes sent in the last call
dt: The time between two calls

This function will return the download speed and upload speed in KB

"""
def track_speed(last_bytes_recv, last_bytes_sent, dt):
    current_net_io = p.net_io_counters()
    delta_upload = current_net_io.bytes_sent - last_bytes_sent
    delta_recv = current_net_io.bytes_recv - last_bytes_recv

    next_time_input_recv = current_net_io.bytes_recv
    next_time_input_sent = current_net_io.bytes_sent

    #KB_speed_upload = int((delta_upload/1024)/dt)
    #KB_speed_recv = int((delta_recv/1024)/dt)

    return delta_upload/dt, delta_recv/dt, next_time_input_recv, next_time_input_sent
