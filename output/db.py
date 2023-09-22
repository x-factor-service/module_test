from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pymysql
import time
import json
import urllib
from multiprocessing import Pool
from sqlalchemy import String
import psycopg2
from psycopg2.extras import execute_values
from plug_decrypt import decrypt_message, load_key

key = load_key()

with open("settings.encrypted", "rb") as f:
    encrypted_data = f.read()

decrypted_data = decrypt_message(encrypted_data, key)
SETTING = json.loads(decrypted_data)

#DB
DBHOST = SETTING['OUTPUT']['DB']['INFO']['HOST']
DBPORT = SETTING['OUTPUT']['DB']['INFO']['PORT']
DBSCHEMA = SETTING['OUTPUT']['DB']['INFO']['SCHEMA']
DBNAME = SETTING['OUTPUT']['DB']['INFO']['NAME']
DBUSER = SETTING['OUTPUT']['DB']['INFO']['USER']
DBPWD = SETTING['OUTPUT']['DB']['INFO']['PWD']
SENSORID = SETTING['INPUT']['API']['TANIUM']['SensorID']['COMMON']

def pg_connect(user, password, db, host, port=5432):
    password = urllib.parse.quote(password, safe='')
    url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine =  create_engine(url, client_encoding='utf8',
    connect_args={'options': """-csearch_path=\"{}\"""".format(DBSCHEMA)})
    return engine

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url)
    return engine

def exportDB(data) :
    # data['disk_total_space'] = data['disk_total_space'].apply(transform_data)
    # data['disk_used_space'] = data['disk_used_space'].apply(transform_data)
    engine = pg_connect(DBUSER, DBPWD, DBNAME, DBHOST, DBPORT)
    try :
        custom_dtype = {
            'id': String(20),
            'cid': String(20),
            'collection_date': String(50)
        }
        try :
            data.to_sql(name='sensor_id_' + SENSORID, con=engine, index=False,
                        dtype=custom_dtype)
        except :
            data.to_sql(name='sensor_id_' + SENSORID, con=engine, if_exists='append', index=False,
                        dtype=custom_dtype)
        print("DB Insert Success")
    except Exception as e :
        print(e)

def exportAPItoDB(data) :
    conn = psycopg2.connect(
        dbname=DBNAME,
        user=DBUSER,
        password=DBPWD,
        host=DBHOST,
        port=DBPORT
    )
    cursor = conn.cursor()

    columns = [col["name"].lower().replace(" ", "_") for col in data["data"]["result_sets"][0]["columns"]]
    rows_data = [tuple(cell[0]["text"] for cell in row["data"]) for row in data["data"]["result_sets"][0]["rows"]]
    print(columns)
    # 테이블 생성 (필요한 경우)
    table_creation_query = f"""CREATE TABLE sensor_id_{SENSORID}_api ({', '.join(['"' + col + '" TEXT' for col in columns])})"""
    cursor.execute(table_creation_query)

    # 데이터를 bulk insert
    insert_query = f"INSERT INTO your_table_name ({', '.join(columns)}) VALUES %s"
    execute_values(cursor, insert_query, rows_data)

    conn.commit()
    conn.close()

def ParallelExport(df) :
    chunks = np.array_split(df, 2)

    with Pool(processes=2) as pool: # 4개의 프로세스를 사용
            pool.map(exportDB, chunks)

def transform_data(data):
    # 딕셔너리 형태의 경우
    if isinstance(data, dict):
        return [f"{k}: {v}" for k, v in data.items()]
    # 집합(set) 또는 리스트 형태의 경우
    elif isinstance(data, (set, list)):
        return list(data)
    # 예외 문자열 형태
    else:
        return [data]