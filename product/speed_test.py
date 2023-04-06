import speedtest

"""
This function will run a Internet speed test and return the download speed, upload speed, and ping
Note: the speed test might take up to 30 seconds, just like the speed test online.
"""

def speed_test():

    st = speedtest.Speedtest()

    #print("Running the Speed test, please wait...")

    download = st.download()
    upload = st.upload()


    servernames =[]
    
    st.get_servers(servernames)

    ping = st.results.ping

    download_unit = " bytes"
    upload_unit = " bytes"

    if download > 1024:
        download = download/1024
        download_unit = " kb"
        if download > 1024:
            download = download/1024
            download_unit = " mb"

    if upload > 1024:
        upload = upload/1024
        upload_unit = " kb"
        if upload > 1024:
            upload = upload/1024
            upload_unit = " mb"

    #print("The download speed is: ",download,download_unit)
    #print("The upload speed is: ",upload,upload_unit)
    #print("The ping is: ",ping," ms")
    return download, download_unit, upload, upload_unit, ping #return download, upload, and ping