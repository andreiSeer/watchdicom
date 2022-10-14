import sqlite3
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


def create_or_start_db():
    con = sqlite3.connect(DATA_BASE)
    cur = con.cursor()  
                
    cur.execute("""CREATE TABLE IF NOT EXISTS study(id INTEGER PRIMARY KEY,
                                                    study_uid VARCHAR(300),
                                                    patient_name VARCHAR(200),
                                                    modality VARCHAR(10),
                                                    datetime_create DATETIME,
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
                                                    datetime_send DATETIME,
                                                    id_serie INTEGER,
                                                    FOREIGN KEY(id_serie) REFERENCES series(id));""")
    con.commit()

class StudyTable:

    
    table_name = "study"

    @staticmethod
    def add_entry(dict_study):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        cur.execute("""INSERT INTO study(id,
                                        study_uid,
                                        patient_name,
                                        modality,
                                        datetime_create,
                                        patient_id) VALUES(?,?,?,?,?,?)""",[None,dict_study["study_uid"],dict_study["patient_name"],dict_study["modality"],dict_study["datetime_create"],dict_study["patient_id"]])
        con.commit()
        cur.close()
    

    @staticmethod
    def look_for_entry(study_uid,patient_id):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM study WHERE study_uid='{study_uid}' AND patient_id='{patient_id}'")
        if cur.fetchone():
            cur.close()
            return True
        cur.close()
        return False
       

class SeriesTable:

    
    table_name = "series"

    @staticmethod
    def add_entry(dict_series):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        cur.execute("""INSERT INTO study(id,
                                        series_uid,
                                        dir_path,
                                        id_study) VALUES(?,?,?,?,?,?)""",[None,dict_series["series_uid"],dict_series["dir_path"],dict_series["id_study"]])
        con.commit()
        cur.close()

    @staticmethod
    def look_for_entry(id_study,series_uid):
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM series WHERE id_study='{id_study}' AND series_uid='{series_uid}'")
        if cur.fetchone():
            cur.close()
            return True
        cur.close()
        return False


class DicomTable:
    
    table_name = "dicom"

    @staticmethod
    def add_entry():
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        #cur.execute("INSERT INTO dicom(a,path) VALUES(?,?)",[None,str(forming_path)])
        con.commit()
        cur.close()
        

    @staticmethod
    def look_for_entry():
        con = sqlite3.connect(DATA_BASE)
        cur = con.cursor()
        #cur.execute(f"SELECT * FROM dicom WHERE path='{forming_path}'")
        if cur.fetchone():
            cur.close()
            return True
        cur.close()
        return False

    @staticmethod
    def update_entry():
        pass

    @staticmethod
    def send_dicom_to_pacs():
        pass