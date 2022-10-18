import sqlite3
import datetime
from decouple import config
DATA_BASE = config('DB_NAME',cast=str)

# def look_for_all_on_sendedfaildicom_table():
#     con = sqlite3.connect("db_file_dicom.db")
#     cur = con.cursor()
#     cur.execute(f"SELECT * FROM sendedfaildicom")
#     records = cur.fetchall()
#     cur.close()
#     return records

# def delete_entry_on_sendedfaildicom_table(forming_path):
#     print("DELETING")
#     con = sqlite3.connect("db_file_dicom.db")
#     cur = con.cursor()
#     cur.execute(f"DELETE FROM sendedfaildicom WHERE path='{forming_path}'")   
#     con.commit()
#     cur.close()

#DATETIME SQLITE FORMAT '2007-01-01 10:00:00'   
def create_or_start_db():
    con = sqlite3.connect(DATA_BASE)
    cur = con.cursor()  
                
    cur.execute("""CREATE TABLE IF NOT EXISTS study(id INTEGER PRIMARY KEY,
                                                    study_uid VARCHAR(300),
                                                    patient_name VARCHAR(200),
                                                    modality VARCHAR(10),
                                                    datetime_create TEXT,
                                                    patient_id VARCHAR(100));""")

    cur.execute("""CREATE TABLE IF NOT EXISTS series(
                                                    id INTEGER PRIMARY KEY,
                                                    series_uid VARCHAR(300),                                                    
                                                    dir_path VARCHAR(200),
                                                    id_study INTEGER,
                                                    FOREIGN KEY(id_study) REFERENCES study(id));""")

    cur.execute("""CREATE TABLE IF NOT EXISTS dicom(
                                                    id INTEGER PRIMARY KEY,
                                                    file_path VARCHAR(250),                                                    
                                                    was_send BOOLEAN default 0,
                                                    datetime_send TEXT,
                                                    id_serie INTEGER,
                                                    FOREIGN KEY(id_serie) REFERENCES series(id));""")
    con.commit()
    cur.close()

class StudyTable:
    
    table_name = "study"

    @staticmethod
    def create_data_set(dicom):
        dict_study ={
            "study_uid":str(dicom.StudyInstanceUID),
            "patient_name":str(dicom.PatientName),
            "modality":str(dicom.Modality),
            "patient_id":str(dicom.PatientID),
            "datetime_create":"",
        }

        return dict_study

    @staticmethod
    def add_and_retrieve_entry(dict_study):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()

        search_result = None
        cur.execute(f"SELECT * FROM study WHERE study_uid='{dict_study['study_uid']}' AND patient_id='{dict_study['patient_id']}'")
        search_result = cur.fetchone()
        
        if not search_result:
            dict_study['datetime_create'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")            
            
            cur.execute("""INSERT INTO study(id,
                                            study_uid,
                                            patient_name,
                                            modality,
                                            datetime_create,
                                            patient_id) VALUES(?,?,?,?,?,?)""",[None,dict_study["study_uid"],dict_study["patient_name"],dict_study["modality"],dict_study["datetime_create"],dict_study["patient_id"]])
            
           
            con.commit()
          
            cur.execute(f"SELECT * FROM study WHERE study_uid='{dict_study['study_uid']}' AND patient_id='{dict_study['patient_id']}'")
           
            search_result = cur.fetchone()  
       
        cur.close()
        return search_result    

  
       

class SeriesTable:

    
    table_name = "series"


    @staticmethod
    def create_data_set(result_search_study,dir_path,dicom):
        dict_study ={
            "series_uid":str(dicom.SeriesInstanceUID),
            "dir_path":str(dir_path),
            "id_study":str(result_search_study[0]),         
        }

        return dict_study
    @staticmethod
    def add_and_retrieve_entry(dict_series):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        search_result = None
        cur.execute(f"SELECT * FROM series WHERE id_study='{dict_series['id_study']}' AND series_uid='{dict_series['series_uid']}'")
        search_result = cur.fetchone()
        if not search_result:
            cur.execute("""INSERT INTO series(id,
                                            series_uid,
                                            dir_path,
                                            id_study) VALUES(?,?,?,?)""",[None,dict_series["series_uid"],dict_series["dir_path"],dict_series["id_study"]])
            con.commit()
            cur.execute(f"SELECT * FROM series WHERE id_study='{dict_series['id_study']}' AND series_uid='{dict_series['series_uid']}'")
            search_result = cur.fetchone()
        cur.close()
        return search_result


    @staticmethod
    def look_for_series_entry(series_id):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM series WHERE id='{series_id}'")
        query_result = cur.fetchone()
        cur.close()
        return query_result






class DicomTable:
    #FIELDS 

    # id INTEGER PRIMARY KEY,
    # file_path VARCHAR(250),                                                    
    # was_send BOOLEAN default 0,
    # datetime_send TEXT,
    # id_serie INTEGER,
    # FOREIGN KEY(id_serie) REFERENCES series(id))

    table_name = "dicom"

    @staticmethod
    def create_data_set(id_serie,file_path):
        dict_study ={
            "file_path":str(file_path),
            "id_serie":str(id_serie),                   
        }
        return dict_study

    @staticmethod
    def add_and_retrieve_entry(dict_series):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        search_result = None
        cur.execute("""INSERT INTO dicom(id,
                                        file_path,
                                        was_send,
                                        datetime_send,
                                        id_serie) VALUES(?,?,?,?,?)""",[None,dict_series["file_path"],"0",None,dict_series["id_serie"]])
        con.commit()
        cur.execute(f"SELECT * FROM dicom WHERE file_path='{dict_series['file_path']}' AND id_serie='{dict_series['id_serie']}'")
        search_result = cur.fetchone()
        cur.close()
        return search_result
        

    @staticmethod
    def look_for_entry(file_path,dir_path,msg=None):
       
        con = sqlite3.connect(DATA_BASE)        
        cur = con.cursor()
        cur.execute(f"SELECT * FROM dicom WHERE file_path='{file_path}'")

        if search_dicom:=cur.fetchone():

            cur_serie = con.cursor()         
            cur_serie.execute(f"SELECT * FROM series where dir_path='{dir_path}' AND id='{search_dicom[4]}'")      

            if cur_serie.fetchone():

                print("Found - cant continue")
                cur.close()
                cur_serie.close()

                return True

            else:

                cur_serie.close()
                print("Series not found - can continue")       

        else:

            print("Dicom not found - can continue")

        cur.close()

        return False

    @staticmethod
    def update_entry(file_path,update_value="1"):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        was_send = update_value
        seding_date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(f"UPDATE dicom SET was_send='{was_send}',datetime_send='{seding_date}'  WHERE file_path='{file_path}'")
        con.commit()
        cur.close()
        


    @staticmethod
    def sended_failed_dicom_file():

        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        was_send = "0"
        trying_resend = "1"
        cur.execute(f"SELECT * FROM dicom WHERE was_send in ('{was_send}', '{trying_resend}')")
        records = cur.fetchall()
        cur.close()
        return records

    @staticmethod
    def sended_all_dicom_file():

        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        was_send = "0"
        cur.execute(f"SELECT * FROM dicom")
        records = cur.fetchall()
        cur.close()
        return records


    @staticmethod
    def send_dicom_to_pacs():
        pass

    @staticmethod
    def return_allowed_dicoms(all_files_inside_dir,dir_path):

        all_dicom = DicomTable.sended_all_dicom_file()
        new_file_list = []
        for one_dicom in all_dicom:
            if one_dicom[1] in all_files_inside_dir:
               all_files_inside_dir.remove(one_dicom[1])
        
