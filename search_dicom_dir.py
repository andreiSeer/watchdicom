from email.policy import default
import time
import os
import re

from decouple import config
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from sql_call_functions import *
from handle_pacs_connection import *



DEBUG = config('SHOW_FEEDBACK',cast=bool)
IGNORE_PATH_NAME = config('IGNORE_PATH_PATTERN',default="")

def not_dir_exclude(path):
    print(path)
    if IGNORE_PATH_NAME:
        reg = re.compile(f'{IGNORE_PATH_NAME}')
        return reg.match(path) is None
    return True




def check_file(filename): 
    
    try: 
        if not_dir_exclude(filename) and check_if_file_is_dicom_and_return(filename) is not None:

            dir_path = os.path.dirname(filename) 

            #TODO: Replace for Regex verification
      
            all_files_inside_dir = os.listdir(dir_path)  
            
            dicom_file = os.path.basename(filename)

            if not DicomTable.look_for_entry(dicom_file,dir_path):
                DicomTable.return_allowed_dicoms(all_files_inside_dir,dir_path)

                for one_inside_dir in all_files_inside_dir:
                    file_path = f"{dir_path}/{one_inside_dir}"

                    if dicom:=check_if_file_is_dicom_and_return(file_path):    

                        result_search_study=StudyTable.add_and_retrieve_entry(StudyTable.create_data_set(dicom))
                        result_search_series = SeriesTable.add_and_retrieve_entry(SeriesTable.create_data_set(result_search_study,dir_path,dicom))                            
                        DicomTable.add_and_retrieve_entry(DicomTable.create_data_set(result_search_series[0],one_inside_dir))
                        store_scu(dicom,one_inside_dir)

                if (DEBUG):
                    print("----------------------------------------------------------------------------")                       
            else:
                if DEBUG:
                    print("Dicom Already Present Outside")
        else:
            if DEBUG:
                print("Não é DICOM")
    
    except Exception as e:
        if DEBUG:
            print("Error ",e)


if __name__ == "__main__":

    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    create_or_start_db()
    # import required module
    from pathlib import Path

    for root, dirs, files in os.walk(config('PATH_DIR')):
        if DEBUG:
            print(root, dirs, files)
            print("----")
        for filename in files:
            if DEBUG:
                print(os.path.join(root, filename))
            check_file(os.path.join(root, filename))

