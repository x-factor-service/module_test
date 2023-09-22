import json
import requests
import sys
from plug_decrypt import decrypt_message, load_key

key = load_key()

with open("settings.encrypted", "rb") as f:
    encrypted_data = f.read()

decrypted_data = decrypt_message(encrypted_data, key)
SETTING = json.loads(decrypted_data)
    
APIURL = SETTING['INPUT']['API']['TANIUM']['URL']
AUTH = SETTING['INPUT']['API']['TANIUM']['PATH']['AUTH']
SAVEDQUESTION = SETTING['INPUT']['API']['TANIUM']['PATH']['SAVEQUSTION']
SENSORID = SETTING['INPUT']['API']['TANIUM']['SensorID']['COMMON']

class API :
    def __init__(self, SessionKey) :
        self.SK = SessionKey
        self.URL = APIURL
        # self.SENSOR = SAVEDQUESTION
        self.HEADER = {'session' : SessionKey}

    def GetApi(self) :
        apiUrl = APIURL + SAVEDQUESTION + SENSORID
        try :
            CallApi = requests.get(url=apiUrl, headers=self.HEADER, verify=False, timeout=60)
            status = CallApi.status_code
            if status == 200 :
                DecodeData = CallApi.content.decode('utf-8')
                ParseData = json.loads(DecodeData)
                # if '[current result unavailable]' in ParseData['data']
            elif status == 404 :
                print("SensorID : {} 가 존재하지 않습니다.".format(SENSORID))
                sys.exit("에러로 인한 모듈 종료")
            else :
                print("[에러] StatusCode : {}".format(status))
                sys.exit("에러로 인한 모듈 종료")
        except Exception as e :
            print(e)
        return ParseData
    

def accountToken(auth, apiUrl) :
    try :
        session = requests.get(url=apiUrl, auth=(auth['Username'], auth['Password']), verify=False)
        status = session.status_code
        if status == 200 :
            SessionKey = session.content.decode('utf-8')
        else :
            print("[에러] StatusCode : {}".format(status))
    except Exception as e :
        print(e)
        # 예외처리 필요
    return SessionKey
