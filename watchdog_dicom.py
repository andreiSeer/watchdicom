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
from decouple import config

ADDR = config('ADDRESS',cast=str)
PORT = config('PORT',cast=int)
AETITLE = config('AETITLE',cast=str)
DEBUG = config('SHOW_FEEDBACK',cast=bool)
IGNORE_PATH_NAME = config('IGNORE_PATH_NAME',cast=str) 


def on_created(event): 
    print("Aqui") 
    try: 
        if PDCM.read_file(event.src_path,force=True):
            dicom = PDCM.read_file(event.src_path)
            if dicom.StudyInstanceUID:

                con = sqlite3.connect("db_file_dicom.db")
                cur = con.cursor()
                reg = re.compile(f'^{IGNORE_PATH_NAME}*')
                #dir_path = os.path.dirname(event.src_path)
                dir_path = [x for x in  os.path.dirname(event.src_path) if not reg.match(x)]
                # [x for x in os.lisdir(path) if not reg.match(x)]
                if not IGNORE_PATH_NAME in dir_path:


                    all_files_inside_dir = os.listdir(dir_path)
                    
                    for one_file_inside in all_files_inside_dir:
                        # print(f"{IGNORE_PATH_NAME} {dir_path}")
                        # if IGNORE_PATH_NAME in dir_path:
                        #     continue
                        forming_path = f"{dir_path}/{one_file_inside}"

                        if PDCM.read_file(forming_path,force=True):
                            dicom = PDCM.read_file(forming_path,force=True)
                        
                            if dicom.StudyInstanceUID:

                                cur.execute(f"SELECT * FROM sendeddicom WHERE path='{forming_path}'")
                                if cur.fetchone():
                                    if DEBUG:
                                        print("Já existe")
                                    continue
                                else:
                                    ae = AE(ae_title=AETITLE)
                                    ae.requested_contexts = StoragePresentationContexts
                                    assoc = ae.associate(ADDR, PORT, ae_title=AETITLE)
                                    if assoc.is_established:
                                        try:
                                            print(f"Enviando imagem do paciente {dicom.PatientName}")
                                            status = assoc.send_c_store(dicom)
                                            if status:
                                                if DEBUG:
                                                    print(f"send {str(forming_path)}")
                                                print(f"Imagem do paciente {dicom.PatientName} enviada")
                                                cur.execute("INSERT INTO sendeddicom(a,path) VALUES(?,?)",[None,str(forming_path)])
                                                con.commit()
                                        except Exception as e:
                                            if DEBUG:
                                                print("Failed", e)
                                    else:
                                        print(f"Falha no envido da imagem do paciente {dicom.PatientName}")
                                        if DEBUG:
                                            print("Association lost.")
                                        cur.execute(f"SELECT * FROM sendedfaildicom WHERE path='{forming_path}'")
                                        if not cur.fetchone():
                                            cur.execute("INSERT INTO sendedfaildicom(a,path) VALUES(?,?)",[None,str(forming_path)])
                                            con.commit()                                        
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
    cur.execute("CREATE TABLE IF NOT EXISTS sendedfaildicom(a INTEGER PRIMARY KEY,path VARCHAR(200));")
    con.commit()
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