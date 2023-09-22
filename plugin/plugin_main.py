from config.token import accountToken, API
from plugin.trans import TransPandas
from output.config import ExportData
from multiprocessing import Pool
from time import sleep
from datetime import datetime
import asyncio
import os
import json
from plugin.seperate_data import seperateTable
from tqdm import tqdm
from plug_decrypt import decrypt_message, load_key

key = load_key()

with open("settings.encrypted", "rb") as f:
    encrypted_data = f.read()

decrypted_data = decrypt_message(encrypted_data, key)
SETTING = json.loads(decrypted_data)
#DB
SENSORID = SETTING['INPUT']['API']['TANIUM']['SensorID']['COMMON']
USERNAME = SETTING['INPUT']['API']['TANIUM']['USERNAME']
PWD = SETTING['INPUT']['API']['TANIUM']['PASSWORD']
APIURL = SETTING['INPUT']['API']['TANIUM']['URL']
URL_AUTH = SETTING['INPUT']['API']['TANIUM']['PATH']['AUTH']
AUTOCREATE = SETTING['OUTPUT']['DB']['AUTOCREATE']
APIINSERT = SETTING['OUTPUT']['DB']['APINSERT']


class puctuation :
    def classfication() :
        global SessionKey
        auth = {"Username":USERNAME, "Password":PWD}
        authUrl = APIURL + URL_AUTH
        SessionKey = accountToken(auth, authUrl)
        data = puctuation.getData(SessionKey)
        if APIINSERT :
            ExportData(data)
            quit()
        ClassifiedData = puctuation.Classfiction(data)
        RefinedData = puctuation.Refind(ClassifiedData)
        if AUTOCREATE :
            transPands = TransPandas(RefinedData)
        else :
            transPands = TransPandas(RefinedData)
            seperatePandas = seperateTable(transPands)
            quit()
        exportData = ExportData(transPands)

    def getData(SessionKey) :
        CallApi = API(SessionKey)
        data = CallApi.GetApi()
        return data

    def extract_values(item):
        now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        id = item["id"]
        cid = item["cid"]
        texts = [sublist[0]['text'] if len(sublist) == 1 else [text_item['text'] for text_item in sublist] for sublist in item['data']]
        return [id]+[cid] + texts + [now]

    def Classfiction(ParseData) :
        hash_list = {1511329504 : 'installed_applications', 4055028299 : 'cpu_details',
                     3200371050 : 'listen_port', 93198492 : 'open_ssh'}
        # Count = len(ParseData['data']['result_sets'][0]['rows'])
        try :
            Data = ParseData['data']['result_sets'][0]['rows']
        except Exception as e :
            if 'rows' in str(e) :
                print("Request SavedQuestion : {}".format(SENSORID))
                asyncio.run(puctuation.requesting())
                ParseData = puctuation.getData(SessionKey)
                Data = ParseData['data']['result_sets'][0]['rows']
        DecodeData = ParseData['data']['result_sets'][0]['columns']
        column_list = []
        for i in DecodeData :
            column = i['name'].strip().replace(' ', '_')
            #중복방지
            #테니엄의 해쉬값과 일치하면 앞에 센서명을 붙인후 '_' 처리
            if i['hash'] in hash_list:
                column = hash_list[i['hash']] + "_" + column

            column_list.append(column.lower())
        DataDict = {
            # 'count' : Count,
            'data' : Data,
            'column' : column_list
        }

        return DataDict

    def Refind(ClassifiedData) :
        cpu_cnt = os.cpu_count()
        print("전체 CPU 개수 : {}".format(cpu_cnt))

        # count = ClassifiedData['count']
        dataList = ClassifiedData['data']
        column = ClassifiedData['column']
        with Pool(cpu_cnt) as pool:
            ids = pool.map(puctuation.extract_values, dataList)
        column = [i.lower() for i in column]

        column.insert(0, 'id')
        column.insert(1, 'cid')
        column.append('collection_date')

        ids.insert(0, column)

        return ids

    async def requesting() :
        with tqdm(total=5, desc="Requesting API") as pbar:
            for i in range(5):
                await asyncio.sleep(1)
                pbar.update(1)

    def classfication_api() :
        return None
        
    def classfication_db() :
        return None