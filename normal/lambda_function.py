import json
import mysql.connector
import datetime

config = {
    "user": "xxxx",
    "password": "xxxx",
    "host": "xxxx",
    "database": "xxxx",
    "port": "xxxx"
}

def lambda_handler(event, context):
    try:
        # 1. 요청 구문 parsing 및 validation check.
        print(event)
        langCode = event['queryStringParameters']['languageCode']
        errorCode = event['pathParameters']['code']

        # reqParam = event["param"]
        # reqParam["languageCode"]

        if langCode == "en":
            col = "DESC_EN"
        elif langCode == "kr":
            col = "DESC_KR"
        elif langCode == "":
            return response(500, 'Please enter languagecode', {})

        else:
            return response(500, 'Wrong language code', {})

        sql = "SELECT ERR_CODE , " + col + " FROM errorcode.ERR_G_CODE_MSTR WHERE ERR_CODE = '" + errorCode + "'"
        print(sql)

        # 2. DB 연결
        conn = mysql.connector.connect(**config)
        print(conn)
        cursor = conn.cursor()
        cursor.execute(sql)
        resultList = cursor.fetchall()

        info = None;

        for result in resultList:
            info = {"errCode":result[0] , "desc":result[1]}

        if info is not None:
            return response(200, 'OK', info)
        else:
            return response(500, 'Wrong error code. We have no description about input error code.', {})


    except mysql.connector.Error as err:
        print(err)
        return response(500, 'Interner error', {})


def response(rspCode, rspMsg, rsp):

    return {
        "isBase64Encoded": "false",
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({
            'rspTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rspCode': rspCode,
            'rspMsg': rspMsg,
            'rsp': rsp
        })
    }
