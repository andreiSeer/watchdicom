import time
import os

from decouple import config
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from sql_call_functions import *
from handle_pacs_connection import *



DEBUG = config('SHOW_FEEDBACK',cast=bool)
IGNORE_PATH_NAME = "HELLO"


def on_created(event): 
    
    try: 
        if check_if_file_is_dicom_and_return(event.src_path) is not None:

            dir_path = os.path.dirname(event.src_path) 

            #TODO: Replace for Regex verification
            if not IGNORE_PATH_NAME in dir_path:
                all_files_inside_dir = os.listdir(dir_path)                
                
                if not DicomTable.look_for_entry(os.path.basename(event.src_path),dir_path):
                    
                    for one_inside_dir in all_files_inside_dir:

                        if not DicomTable.look_for_entry(one_inside_dir,dir_path,"internos"):

                            file_path = f"{dir_path}/{one_inside_dir}"

                            if dicom:=check_if_file_is_dicom_and_return(file_path): 
                                                        
                                result_search_study=StudyTable.add_and_retrieve_entry(StudyTable.create_data_set(dicom))
                                result_search_series = SeriesTable.add_and_retrieve_entry(SeriesTable.create_data_set(result_search_study,dir_path,dicom))                            
                                DicomTable.add_and_retrieve_entry(DicomTable.create_data_set(result_search_series[0],one_inside_dir))
                                store_scu(dicom,one_inside_dir)

                                #print(result_search_dicom)
                        else:
                            print("Dicom Already Present Inside")     
                    print("----------------------------------------------------------------------------")                       
                else:
                    print("Dicom Already Present Outside")
        else:
            print("Não é DICOM")
    
    except Exception as e:
        print("Error ",e)


if __name__ == "__main__":

    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    create_or_start_db()
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

my_event_handler.on_created = on_created
path = config('PATH_DIR',cast=str)
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)
my_observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()