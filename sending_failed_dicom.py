import time
from decouple import config
from sql_call_functions import *

DEBUG = config('SHOW_FEEDBACK',cast=bool)
WAIT_TIME = config('WAIT_TIME',cast=int)



while True:
    all_records_on_failed_table = look_for_all_on_sendedfaildicom_table()
    for row in all_records_on_failed_table:
        forming_path = row[1]
        if look_for_entry_on_sendeddicom_table(forming_path) is False:
            if PDCM.read_file(forming_path,force=True):
                dicom = PDCM.read_file(forming_path,force=True)
                if dicom.StudyInstanceUID:
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
                                add_entry_on_sendeddicom_table(forming_path)
                        except Exception as e:
                            if DEBUG:
                                print("Failed", e)
                    assoc.release()
        else:
            if DEBUG:                
                print("Já enviado")
            delete_entry_on_sendedfaildicom_table(forming_path)
    time.sleep(WAIT_TIME)