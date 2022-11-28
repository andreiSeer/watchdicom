import time
import subprocess
from decouple import config

from sql_call_functions import *
from handle_pacs_connection import *

DEBUG = config('SHOW_FEEDBACK',cast=bool)
WAIT_TIME = config('WAIT_TIME',cast=int)



while True:
    all_records_on_failed_table = DicomTable.sended_failed_dicom_file()
    print("STARTING FAILED DICOM SERVICE")
    for row in all_records_on_failed_table:

        dicom_file= row[1]
        series_id = row[4]
        dicom_series = SeriesTable.look_for_series_entry(series_id)

        series_uid = dicom_series[1]
        series_dir_path = dicom_series[2]
        file_path = series_dir_path+"/"+dicom_file
        dicom=check_if_file_is_dicom_and_return(file_path)
        if dicom:
            if not store_scu(dicom,dicom_file):
                #command = f'python3 -m pynetdicom storescu {ADDR} {PORT} {file_path} -aec {AETITLE} -d -cx'
                command = "storescu "+ADDR+" "+str(PORT)+" "+file_path+" -aec "+AETITLE+" -xs -nh"
                process = subprocess.run(command, shell=True, capture_output=True)
                if process.stderr:
                    if "I: Received Store Response (Success)" in process.stderr.decode('utf-8'):
                        print("Sucesso")
                        DicomTable.update_entry(dicom_file,"2")
                else:
                    print("Falha")
                    print(process.stderr)
           
                    
            
        


    print("--------------------------------------------------------------")
    time.sleep(WAIT_TIME)
