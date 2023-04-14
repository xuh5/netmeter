from time import sleep
import psutil as p

"""
This is the track speed function, it will calculate the average download and upload speed in a given time slot
the return value of this function will be the next time input
Note: This function is a one-time version of the function above

lastBytesRecv: The value of bytes received in the last call
lastBytesSent: The value of bytes sent in the last call
durationTime: The time between two calls

This function will return the download speed and upload speed in KB

"""
def track_speed(lastBytesRecv, lastBytesSent, durationTime):
    
    currentNetIo = p.net_io_counters() #Initialize the io countings
    
    #Get the difference of io receive and send between this call and last call
    deltaUpload = currentNetIo.bytes_sent - lastBytesSent
    deltaRecv = currentNetIo.bytes_recv - lastBytesRecv

    #Keep the data for next call
    nextTimeInputRecv = currentNetIo.bytes_recv
    nextTimeInputSent = currentNetIo.bytes_sent

    return deltaUpload/durationTime, deltaRecv/durationTime, nextTimeInputRecv, nextTimeInputSent
