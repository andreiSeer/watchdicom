import pydicom as PDCM
from pynetdicom import AE,StoragePresentationContexts
from decouple import config

ADDR = config('ADDRESS',cast=str)
PORT = config('PORT',cast=int)
AETITLE = config('AETITLE',cast=str)
DEBUG = config('SHOW_FEEDBACK',cast=bool)



def check_if_file_is_dicom_and_return(src_path):
    if PDCM.read_file(src_path,force=True):
        dicom = PDCM.read_file(src_path)
        if dicom.StudyInstanceUID:
            return dicom
    print("HERE")
    return None




def store_scu(dicom):
    ae = AE(ae_title=AETITLE)
    assoc = ae.associate(ADDR, PORT, ae_title=AETITLE)
    if assoc.is_established:
        if assoc.is_established:
            try:                
                status = assoc.send_c_store(dicom)
                if status:
                    pass
                    #Add Dicom Entry with send status and date time
            except Exception as e:
                if DEBUG:
                    print("Failed", e)
        else:
      
            if DEBUG:
                print("Association lost.")
            #Add Dicom Entry  with send status False                                    
        assoc.release()
    


# ae = AE(ae_title=AETITLE)
# ae.requested_contexts = StoragePresentationContexts
# assoc = ae.associate(ADDR, PORT, ae_title=AETITLE)
# if assoc.is_established:
#     try:
#         print(f"Enviando imagem do paciente {dicom.PatientName}")
#         status = assoc.send_c_store(dicom)
#         if status:
#             if DEBUG:
#                 print(f"send {str(forming_path)}")
#             print(f"Imagem do paciente {dicom.PatientName} enviada")
#             cur.execute("INSERT INTO sendeddicom(a,path) VALUES(?,?)",[None,str(forming_path)])
#             con.commit()
#     except Exception as e:
#         if DEBUG:
#             print("Failed", e)
# else:
#     print(f"Falha no envido da imagem do paciente {dicom.PatientName}")
#     if DEBUG:
#         print("Association lost.")
#     cur.execute(f"SELECT * FROM sendedfaildicom WHERE path='{forming_path}'")
#     if not cur.fetchone():
#         cur.execute("INSERT INTO sendedfaildicom(a,path) VALUES(?,?)",[None,str(forming_path)])
#         con.commit()                                        
# assoc.release()