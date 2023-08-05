#Wikicivi Crawler Client SDK
import os
import time
import datetime
import os,sys
import json
import re
import logging
import pytz
import copy

class Agfcc:
    #构造函数,必须有日志句柄和error_codes
    def __init__(self,mongo_log_col,error_codes,event_text):
        self.mongo_log_col=mongo_log_col
        self.error_codes  =error_codes
        self.event_text   =event_text
        try:
            event_json = eval(event_text)
        except Exception as err:
            event_json = None
        self.event_json   = event_json
        
    def success(self,result=None):
        return self.exit("success",result)
    def failure(self,reason,result=None):
        return self.exit(reason,result)

    def exit(self,reason,result=None):
        #我们将用logger记录在阿里云日志上
        logger = logging.getLogger()
        #agfcc系统以:隔开主原因和次要原因
        if ":" in reason:
            main_reason = reason.split(":")[0]
            secd_resson = reason.split(":")[1]
        else:
            main_reason = reason
            secd_reason = ""
        
        #分析是否有error_codes字段
        error_codes = self.error_codes
        if error_codes == None:
            error_codes = {"success":0}
        
        if main_reason not in error_codes:
            error = 1
        else:
            error = error_codes[main_reason]
        
        asmrt = {
                "isBase64Encoded":False,
                "statusCode":200,
                "headers":None,
                "body":{"error":error,"reason":reason,"result":result}
                }
        #试着把调用写入日志表,如果写入失败，不要影响
        """
        当以函数计算作为API网关的后端服务时，API网关会把请求参数通过一个固定的Map结构传给函数计算的入参event，
        函数计算通过如下结构去获取需要的参数，然后进行处理，该结构如下：
        {
        "path":"api request path",
        "httpMethod":"request method name",
        "headers":{all headers,including system headers},
        "queryParameters":{query parameters},
        "pathParameters":{path parameters},
        "body":"string of request payload",
        "isBase64Encoded":"true|false, indicate if the body is Base64-encode"
        }
        需要特别说明的是：当isBase64Encoded=true时，
        表明API网关传给函数计算的body内容是经过Base64编码的，
        函数计算需要先对body内容进行Base64解码后再处理。
        反之，isBase64Encoded=false时，表明API网关没有对body内容进行Base64编码。
        下面就是一个典型的evt结构.base64编码的body里就是{'brief': 'what a fuck', 'name': 'test'}
        '{"result":{"headers":{"X-Ca-Api-Gateway":"C66FA93A-5283-4590-9A50-D6FFFFD47B0F",
        "X-Forwarded-For":"159.226.43.36","Content-Type":"application/octet-stream; charset=UTF-8"},
        "body":"eyJicmllZiI6ICJ3aGF0IGEgZnVjayIsICJuYW1lIjogInRlc3QifQ==","pathParameters":{},
        "httpMethod":"POST","path":"/site","isBase64Encoded":true,"queryParameters":{}},"error":1,"reason":"debug"}
        
        下面是一个带上阿里云网关全部系统参量的headers信息：
        {
        "result":{
            "headers":{
                "CaRequestId":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
                "X-Ca-Api-Gateway":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
                "CaProxy":"AliCloudAPIGateway",
                "CaClientUa":"curl/7.61.0",
                "CaApiName":"echo",
                "CaHttpSchema":"HTTP",
                "X-Forwarded-For":"159.226.43.61",
                "CaRequestHandleTime":"2018-11-15T06:11:33Z",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "CaDomain":"api.hannm.com",
                "CaClientIp":"159.226.43.61",
                "CaAppId":"null"
            },
            "body":"",
            "pathParameters":{"echo_text":"phone"},
            "httpMethod":"GET",
            "path":"/echo/phone",
            "isBase64Encoded":false,
            "queryParameters":{},
            "error":0,"reason":"success"
        }
        """
 
        mongo_doc = {
            "incr":int(time.time()*1000000),
            "event":str(self.event_text),
            "return":asmrt,
            #函数计算都装的是格林威治时区的docker,需要自己手动转
            "ctime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()) +3600*8))
        }
       
        try:
            event_json = self.event_json
            mongo_doc["headers"] = event_json["headers"]
            event_json_copy = copy.deepcopy(event_json)
            event_json_copy.pop("headers")
            mongo_doc["params"] = event_json_copy
            logger.info(mongo_doc)
            #不仅记录入阿里云的log,也记录如我们的日志数据库
            self.mongo_log_col.insert_one(mongo_doc)
        except Exception as err:
            logger.error(err)
            print(err) 
        return json.dumps(asmrt, ensure_ascii=False)


    #解码event字符串成event_json
    @staticmethod 
    def devent(event_text):
        #下面是一个带上阿里云网关全部系统参量的headers信息：
        """
        {"result":{
                "headers":{
                    "CaRequestId":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
                    "X-Ca-Api-Gateway":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
                    "CaProxy":"AliCloudAPIGateway",
                    "CaClientUa":"curl/7.61.0",
                    "CaApiName":"echo",
                    "CaHttpSchema":"HTTP",
                    "X-Forwarded-For":"159.226.43.61",
                    "CaRequestHandleTime":"2018-11-15T06:11:33Z",
                    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                    "CaDomain":"api.hannm.com",
                    "CaClientIp":"159.226.43.61",
                    "CaAppId":"null"
                },
                "body":"",
                "pathParameters":{"echo_text":"phone"},
                "httpMethod":"GET",
                "path":"/echo/phone",
                "isBase64Encoded":false,
                "queryParameters":{}
            },
            "error":0,
            "reason":"success"
        }
        """
        try:
            event_json = json.loads(event_text)
            if(event_json["isBase64Encoded"]):
                event_body = base64.b64decode(str(event_json["body"]))
            else:
                event_body = str(event_json["body"])     
            event_json["body"] = event_body
            event_headers = event_json["headers"]
            req_headers = [
                    "CaRequestId",
                    "X-Ca-Api-Gateway",
                    "CaProxy",
                    "CaClientUa",
                    "CaApiName",
                    "CaHttpSchema",
                    "X-Forwarded-For",
                    "CaRequestHandleTime",
                    "Content-Type",
                    "CaDomain",
                    "CaClientIp",
                    "CaAppId"
            ]
            for req_header in req_headers:
                if req_header not in event_headers: raise Exception("缺少系统头参数:"+req_header)
            return True,event_json
        except Exception as err:
            return False,str(err)
