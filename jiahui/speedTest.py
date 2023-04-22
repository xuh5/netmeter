import speedtest

"""
This function will run a Internet speed test and return the download speed, upload speed, and ping

:return: download: the download speed, float
:return: downloadUnit: the unit of download speed, string
:return: upload: the upload speed, float
:return: uploadUnit: the unit of upload speed, string
:return: ping: current ping, int
"""

def speedTest():

    st = speedtest.Speedtest() #Initialize the speed test model

    #print("Running the Speed test, please wait...")

    download = st.download() #Run the download speed test
    upload = st.upload() #Run the upload speed test

    #Get ping
    serverNames =[]
    st.get_servers(serverNames)
    ping = st.results.ping
    
    #Initialize units
    downloadUnit = " bytes"
    uploadUnit = " bytes"
    
    #Convert the value and unit depend on result
    if download > 1024:
        download = download/1024
        downloadUnit = " kb"
        if download > 1024:
            download = download/1024
            downloadUnit = " mb"

    if upload > 1024:
        upload = upload/1024
        uploadUnit = " kb"
        if upload > 1024:
            upload = upload/1024
            uploadUnit = " mb"

    #print("The download speed is: ",download,download_unit)
    #print("The upload speed is: ",upload,upload_unit)
    #print("The ping is: ",ping," ms")
    return download, downloadUnit, upload, uploadUnit, ping #return download, upload, and ping
