import json
import pandas as pd
import os
from plug_decrypt import decrypt_message, load_key

key = load_key()

with open("settings.encrypted", "rb") as f:
    encrypted_data = f.read()

decrypted_data = decrypt_message(encrypted_data, key)
SETTING = json.loads(decrypted_data)
    
FILETYPE = SETTING['OUTPUT']['FILE']['TYPE'].lower()
INDEX = SETTING['OUTPUT']['FILE']['INDEX'].lower()
SAVETYPE = SETTING['OUTPUT']['FILE']['SAVETYPE'].lower()
SHEETSORT = SETTING['OUTPUT']['FILE']['SHEETSORT'].lower()
FILEPATH = SETTING['OUTPUT']['FILE']['PATH']
SENSORID = SETTING['INPUT']['API']['TANIUM']['SensorID']['COMMON']

def exportFile(data) :
    filepath = FILEPATH
    if FILETYPE == 'excel' :
        exportExcel(filepath)
    return None

def exportExcel(filepath) :
    filename = 'sensor_id_' + SENSORID + '.xlsx'
    file = filepath + filename
    sheet_name = 'Sheet1'
    if INDEX == 'true' :
        index = "True"
    elif INDEX == 'false' :
        index = "False"
    if SAVETYPE == 'overwrite' :
        savetype = ''
    if SAVETYPE == 'insert' :
        if os.path.exists(file) :
            if SHEETSORT == 'true' :
                with pd.ExcelWriter(file, mode='a') as writer:
                    xls = pd.ExcelFile(file)
                    data['collection_date'] = pd.to_datetime(data['collection_date'])
                    sheet_name = data['collection_date'].dt.date.iloc[0].strftime('%Y-%m-%d')
                    if sheet_name in xls.sheet_names:
                        existing_data = pd.read_excel(xls, sheet_name)
                        combined_data = pd.concat([existing_data, data], ignore_index=True)
                        combined_data.to_excel(writer, sheet_name=sheet_name, index=index)
                    else :
                        sheet_name = sheet_name
            elif SHEETSORT == 'false' :
                existing_data = pd.read_excel(file)
                combined_data = pd.concat([existing_data, data], ignore_index=True)
                data = combined_data
    data.to_excel(file, index=index, sheet_name=sheet_name)