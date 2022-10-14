import sqlite3


# def add_entry_on_sendeddicom_table(forming_path):
#     con = sqlite3.connect("db_file_dicom.db")
#     cur = con.cursor()
#     cur.execute("INSERT INTO sendeddicom(a,path) VALUES(?,?)",[None,str(forming_path)])
#     con.commit()
#     cur.close()


# def add_entry_on_sendedfaildicom_table(forming_path):
#     con = sqlite3.connect("db_file_dicom.db")
#     cur = con.cursor()
#     cur.execute("INSERT INTO sendedfaildicom(a,path) VALUES(?,?)",[None,str(forming_path)])
#     con.commit()
#     cur.close()

# def look_for_entry_on_sendeddicom_table(forming_path):
#     con = sqlite3.connect("db_file_dicom.db")
#     cur = con.cursor()
#     cur.execute(f"SELECT * FROM sendeddicom WHERE path='{forming_path}'")
#     if cur.fetchone():
#         cur.close()
#         return True
#     cur.close()
#     return False
    

# def look_for_entry_on_sendedfaildicom_table(forming_path):
#     con = sqlite3.connect("db_file_dicom.db")
#     cur = con.cursor()
#     cur.execute(f"SELECT * FROM sendedfaildicom WHERE path='{forming_path}'")
#     if cur.fetchone():
#         cur.close()
#         return True
#     cur.close()
#     return False

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


    