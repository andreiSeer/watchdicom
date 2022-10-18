import time

import pydicom as PDCM
from pynetdicom import AE,StoragePresentationContexts
from decouple import config
from pydicom.uid import RLELossless

from sql_call_functions import DicomTable

ADDR = config('ADDRESS',cast=str)
PORT = config('PORT',cast=int)
AETITLE = config('AETITLE',cast=str)
DEBUG = config('SHOW_FEEDBACK',cast=bool)



def check_if_file_is_dicom_and_return(src_path):
    time.sleep(5)
    if dicom:=PDCM.read_file(src_path,force=True):        
        if dicom.StudyInstanceUID:
            #try:
            return dicom
            #except Exception as e:
                #print(e)
                #return dicom    
    return None




def store_scu(dicom,one_inside_dir):
    
    ae = AE(ae_title=AETITLE)
    ae.requested_contexts = StoragePresentationContexts
    assoc = ae.associate(ADDR, PORT, ae_title=AETITLE)    
   
    if assoc.is_established:
        try: 
            DicomTable.update_entry(one_inside_dir,"1")            
            status = assoc.send_c_store(dicom)
            print("ENVIANDO ", one_inside_dir)
            if status:
                DicomTable.update_entry(one_inside_dir,"2")
                return True              
        except Exception as e:
            if DEBUG:
                print("Failed", e)
    else:      
        if DEBUG:
            print("Association lost.")                                             
    assoc.release() 
    return False


