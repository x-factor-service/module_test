import json
from output.api import *
from output.db import ParallelExport, exportDB, exportAPItoDB
from output.file import exportFile
from plug_decrypt import decrypt_message, load_key

key = load_key()

with open("settings.encrypted", "rb") as f:
    encrypted_data = f.read()

decrypted_data = decrypt_message(encrypted_data, key)
SETTING = json.loads(decrypted_data)
    
DBUSE = SETTING['OUTPUT']['DB']['USE']
APIUSE = SETTING['OUTPUT']['API']['USE']
FILEUSE = SETTING['OUTPUT']['FILE']['USE']
APIINSERT = SETTING['OUTPUT']['DB']['APINSERT']

def ExportData(data) :
    if DBUSE :
        if APIINSERT :
            exportAPItoDB(data)
        else :
            exportDB(data)
    if APIUSE :
        return None
    if FILEUSE :
        exportFile(data)
    # elif APIUSE == 'true' :
    # elif CSVUSE == 'true' :
    # elif JSONUSE == 'true' :
    return None