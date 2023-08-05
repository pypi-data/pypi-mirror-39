import requests
import json

from .utils import *

http_headers = {"Content-type":"application/json"}

def doTask(taskUrl,serverName,data):
    data = json.dumps({'server_name':serverName,'traffic_paramsDict':data})
    ret = requests.post(taskUrl,data,headers=http_headers)
    response_status = ret.status_code
    if response_status == 200:
        result = json.loads(ret.text)
        if result['status']==True:
            return result['result']
        return None
    else:
        printException('response error with status code:%s '%response_status)
        return None

