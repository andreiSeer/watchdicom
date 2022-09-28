import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import pydicom as PDCM
import subprocess
import sqlite3
import os
import sqlite3
ADDR = ''
PORT = 11112
AETITLE = ''


# blank_db = sqlite3.connect('/home/develop4/Desktop/higia_projects/watchdog_dicom/test2.db')
# cur = blank_db.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS senderror(a INTEGER PRIMARY KEY,path VARCHAR(200));")
     
# blank_db.commit()
# cur.close()
   

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):  
    
    try: 
        if PDCM.dcmread(event.src_path):
            dicom = PDCM.dcmread(event.src_path)
            if dicom.StudyInstanceUID:

                con = sqlite3.connect("db_file_dicom.db")
                cur = con.cursor()                
                cur.execute("CREATE TABLE IF NOT EXISTS senderror(a INTEGER PRIMARY KEY,path VARCHAR(200));")
                con.commit()

                dir_path = os.path.dirname(event.src_path)
                all_files_inside_dir = os.listdir(dir_path)
                
                for one_file_inside in all_files_inside_dir:

                    forming_path = f"{dir_path}/{one_file_inside}"

                    if PDCM.dcmread(forming_path):
                        dicom = PDCM.dcmread(forming_path)
                        if dicom.StudyInstanceUID:

                            cur.execute(f"SELECT * FROM senderror WHERE path='{one_file_inside}'")
                            if cur.fetchone():
                                print("Já existe")
                                continue
                            else:
                                # command = f'python3 -m pynetdicom storescu {ADDR} {PORT} {event.src_path} -aec {AETITLE} -d'
                                # process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                                # output, error = process.communicate()
                                # print(output)
                                # print(error)
                                #if error is not None:
                                cur.execute("INSERT INTO senderror(a,path) VALUES(?,?)",[None,str(one_file_inside)])
                                con.commit()
                cur.close()
            
          
          
    
    except Exception as e:
        print("Error ",e)
    


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