import pydicom as PDCM
from pynetdicom import AE,StoragePresentationContexts
from decouple import config

ADDR = config('ADDRESS',cast=str)
PORT = config('PORT',cast=int)
AETITLE = config('AETITLE',cast=str)
DEBUG = config('SHOW_FEEDBACK',cast=bool)




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
    