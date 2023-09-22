import os
import time
import json
from plugin.plugin_main import puctuation
from plugin.decode import decodeJson
import threading
# import consumer


def handle_message(message):
    dataDict = decodeJson(message)
    if dataDict['INAPI']:
        puctuation.classfication(dataDict)
    if dataDict['INDB']:
        puctuation.classfication_db()

def main():
    puctuation.classfication()
    # channel = consumer.initialize()

    # while True:  # 이 프로그램을 계속 실행하도록 무한 루프
    #     consumer.wait_for_message(channel)  # 메시지가 도착할 때까지 기다립니다.
    #     handle_message(consumer.receivedMessage)  # 메시지 처리
    #     consumer.receivedMessage = None  # 메시지 상태를 초기화합니다.

if __name__ == "__main__":
    print("Start Module")
    
    start = time.time()
    main()
    end = time.time()

    print("수행시간: %f 초" % (end - start))
    print("End Module")