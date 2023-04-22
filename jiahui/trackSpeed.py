from time import sleep
import psutil as p

"""
This is the track speed function, it will calculate the average download and upload speed in a given time slot
the return value of this function will be the next time input

:param: lastBytesRecv: The value of bytes received in the last call, unsigned int
:param: lastBytesSent: The value of bytes sent in the last call, unsigned int
:param: durationTime: The time between two calls, float

:return: avgUpload: the average upload speed in the duration, float
:return: avgDownload: the average download speed in the duration, float
:return: nextTimeInputRecv: the input value of received bytes in the next call, unsigned int
:return: nextTimeInputSent: the input value of sent bytes in the next call, unsigned int

"""
def trackSpeed(lastBytesRecv, lastBytesSent, durationTime):
    
    currentNetIo = p.net_io_counters() #Initialize the io countings
    
    #Get the difference of io receive and send between this call and last call
    deltaUpload = currentNetIo.bytes_sent - lastBytesSent
    deltaRecv = currentNetIo.bytes_recv - lastBytesRecv

    #Keep the data for next call
    nextTimeInputRecv = currentNetIo.bytes_recv
    nextTimeInputSent = currentNetIo.bytes_sent
    
    avgUpload = deltaUpload/durationTime
    avgDownload = deltaRecv/durationTime

    return avgUpload, avgDownload, nextTimeInputRecv, nextTimeInputSent
