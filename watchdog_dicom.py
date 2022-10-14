import time
import sqlite3
import os
from decouple import config

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from sql_call_functions import *
from handle_pacs_connection import *



DEBUG = config('SHOW_FEEDBACK',cast=bool)
IGNORE_PATH_NAME = config('IGNORE_PATH_PATTERN',cast=str) 


def on_created(event): 
    
    try: 
        if check_if_file_is_dicom_and_return(event.src):            

            con = sqlite3.connect(DATA_BASE)
            cur = con.cursor()   
            dir_path = os.path.dirname(event.src_path)        
       
            if not IGNORE_PATH_NAME in dir_path:
                all_files_inside_dir = os.listdir(dir_path)                
                for one_file_inside in all_files_inside_dir:          
                    forming_path = f"{dir_path}/{one_file_inside}"

                    if dicom:=check_if_file_is_dicom_and_return(event.src):                        

                        cur.execute(f"SELECT * FROM sendeddicom WHERE path='{forming_path}'")
                        if cur.fetchone(dicom):
                            if DEBUG:
                                print("Já existe")
                            continue
                        else:
                            store_scu()
                            pass
                cur.close()
    
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