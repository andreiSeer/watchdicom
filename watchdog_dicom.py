import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import pydicom as PDCM
from pynetdicom import (
    AE,
    StoragePresentationContexts
)
import sqlite3
import os
ADDR = ''
PORT = 000000
AETITLE = ''

def on_created(event):  
    
    try: 
        if PDCM.read_file(event.src_path,force=True):
            dicom = PDCM.read_file(event.src_path)
            if dicom.StudyInstanceUID:

                con = sqlite3.connect("db_file_dicom.db")
                cur = con.cursor()

                dir_path = os.path.dirname(event.src_path)
                all_files_inside_dir = os.listdir(dir_path)
                
                for one_file_inside in all_files_inside_dir:

                    forming_path = f"{dir_path}/{one_file_inside}"

                    if PDCM.read_file(forming_path,force=True):
                        dicom = PDCM.read_file(forming_path,force=True)
                     
                        if dicom.StudyInstanceUID:

                            cur.execute(f"SELECT * FROM sendeddicom WHERE path='{forming_path}'")
                            if cur.fetchone():
                                print("Já existe")
                                continue
                            else:
                                ae = AE(ae_title=str(AETITLE))
                                ae.requested_contexts = StoragePresentationContexts
                                assoc = ae.associate(ADDR, PORT, ae_title=AETITLE)
                                if assoc.is_established:
                                    try:
                                        status = assoc.send_c_store(dicom)
                                        if status:
                                            print("Dicom Enviado")
                                            cur.execute("INSERT INTO sendeddicom(a,path) VALUES(?,?)",[None,str(forming_path)])
                                            con.commit()
                                    except:
                                        print("Failed")
                                if not assoc.is_released:
                                    assoc.release()
                               
                cur.close()
    
    except Exception as e:
        print("Error ",e)


if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    con = sqlite3.connect("db_file_dicom.db")
    cur = con.cursor()                
    cur.execute("CREATE TABLE IF NOT EXISTS sendeddicom(a INTEGER PRIMARY KEY,path VARCHAR(200));")
    con.commit()
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

my_event_handler.on_created = on_created
path = "."
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