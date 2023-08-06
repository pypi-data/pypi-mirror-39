#!/usr/bin/env python
#encoding: utf-8
# Author: colinspace
# Date: 2018
# Desc:
#

from yunpian_python_sdk.ypclient import YunpianClient
from yunpian_python_sdk.model import constant as YC

from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import SendBatchSmsRequest
from aliyunsdkcore.profile import region_provider

import urllib.parse
import configparser
import uuid

import serverMonitor


class SMS():
    """
    @param: sms_config_file:  sms.conf config file 
    @param: mobile
    @param: content
    @return: sendstatus

    ## warn
    告警 - 资源[${resource}]；当前值[${currentValue}] - 阈值[${threshold}]；备注：${remark}
    {"resouce": "cpu", "currentValue": "95%", "threshold": "80%", "remark": "192.168.2.52 4core"}

    ## recovery
    恢复 - 资源[${resource}]；当前值[${currentValue}]；备注：${remark}
    {"resouce": "cpu", "currentValue": "2.3%", "remark": "192.168.2.4"}
    """

    def __init__(self, sms_config_file='/etc/.sms.conf',section='sms', mobile=None, content=None, smstype='warn'):
        self.sms_config_file = sms_config_file
        self.section = section
        self.mobile = mobile
        self.content = content
        self.smstype = smstype



    def getYunpianConfig(self):
        config = configparser.ConfigParser()
        config.read(self.sms_config_file)
        return config['yunpiansms']['api_key']

    def getAliyunConfig(self):
        aliyunsms = {}
        config = configparser.ConfigParser()
        config.read(self.sms_config_file)
        aliyunsms['access_keyid'] = config[self.section]['access_keyid']
        aliyunsms['access_keysecret'] = config[self.section]['access_keysecret']
        aliyunsms['template_code_warn'] = config[self.section]['template_code_warn']
        aliyunsms['template_code_recovery'] = config[self.section]['template_code_recovery']
        aliyunsms['sign_name'] = config[self.section]['sign_name']
        # aliyunsms['UID'] = config['aliyunsms']['UID']
        return aliyunsms

 
    def yunpiansms(self):
        """
        云片短信发送
        内容模板：
        {"resource": "CPU", "detail": "the detail of warning info", "remark": "could be empty"}
        """
        msg = {}
        apikey = self.getYunpianConfig()
        client = YunpianClient(apikey)

        # mobile template id
        if self.smstype == 'warn':
            template_id =  2651642
        elif self.smstype == 'recovery':
            template_id =  2651644

        # template_id = 2265948

        # mobile template value
        template_value = urllib.parse.urlencode(eval(self.content)) 

        # build param
        param = {YC.MOBILE:self.mobile, YC.TPL_ID:template_id, YC.TPL_VALUE:template_value}

        # single or batch to send 
        if len(self.mobile.split(',')) > 1:
            result = client.sms().tpl_batch_send(param)
        else:
            result = client.sms().tpl_single_send(param)

        # check if send successful
        if result.code() == 0:
            msg['status'] = 200
            msg['content'] = "Warninig send sucessfully!"
        else:
            msg['status'] = 500
            msg['content'] = "Sorry, send sms failed! Exception like: %s" % res.exception

        return msg 


    

    def aliyunSMS(self):
        """
        阿里云发送短信
        """
        msg = []

        REGION = "cn-hangzhou"
        PRODUCT_NAME = "Dysmsapi"
        DOMAIN = "dysmsapi.aliyuncs.com"

        aliyunconfig = self.getAliyunConfig()
        access_keyid = aliyunconfig['access_keyid']
        access_keysecret = aliyunconfig['access_keysecret']
        template_code_warn = aliyunconfig['template_code_warn']
        template_code_recovery = aliyunconfig['template_code_recovery']
        sign_name = aliyunconfig['sign_name']
        # uid = aliyunconfig['UID']
        uid = uuid.uuid1()

        acs_client = AcsClient(access_keyid, access_keysecret, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
        if self.smstype == 'warn':
            template_code = template_code_warn
        elif self.smstype == 'recovery':
            template_code = template_code_recovery
        smsRequest = SendSmsRequest.SendSmsRequest()
        smsRequest.set_TemplateCode(template_code)
        smsRequest.set_SignName(sign_name) 
        smsRequest.set_OutId(uid)
        smsRequest.set_TemplateParam(self.content)

        for number in self.mobile.split(','):
            msg_temp = {}
            smsRequest.set_PhoneNumbers(number)
            smsResponse = eval(acs_client.do_action_with_exception(smsRequest).decode('utf-8'))
            if smsResponse['Message'] == 'OK':
                msg_temp['status'] = 200
                msg_temp['content'] = "send sucessfully!"
            else:
                msg_temp['status'] = 500
                msg_temp['content'] = "Sorry, send sms failed! Exception like: %s" % smsResponse['Message']
            msg.append(msg_temp)

        # if len(self.mobile.split(',')) > 1:
        #     for number in self.mobile.split(','):
        #         smsRequest.set_PhoneNumbers(number)
        #         smsResponse = eval(acs_client.do_action_with_exception(smsRequest).decode('utf-8'))
        # else:
        #     smsRequest.set_PhoneNumbers(self.mobile)
        #     smsResponse = eval(acs_client.do_action_with_exception(smsRequest).decode('utf-8'))
        # print(type(smsResponse))
        # print(smsResponse)
        # if smsResponse['Message'] == 'OK':
        #     msg['status'] = 200
        #     msg['content'] = "send sucessfully!"
        # else:
        #     msg['status'] = 500
        #     msg['content'] = "Sorry, send sms failed! Exception like: %s" % smsResponse.Message
        return msg 


if __name__ == '__main__':
    aliyunsms = SMS()
    aliyunsms.sms_config_file = '/data/colinspace/sms.conf'
    aliyunsms.section = 'zhuoyuansms'
    # aliyunsms.section = 'aliyunsms'
    aliyunsms.mobile = '13269675859,15810610185'
    # aliyunsms.UID = '279208526974282824'
    # aliyunsms.UID = uuid.uuid1()
    server = serverMonitor.Server()
    server.threshold = 10
    result = server.checkDisk()
    aliyunconfig = aliyunsms.getAliyunConfig()
    print(aliyunconfig)

    # if result:
       #  content = result['detail']
    # aliyunsms.content = """ {"resource":"disk", "detail":"%s","remark":""}""" % content


    if result:
        resource = result['resource']
        currentValue = result['currentValue']
        threshold = result['threshold']
        remark = result['remark']
        detail = result['detail']
        # aliyunsms.content = """ {"resource": "%s", "currentValue":"%s", "threshold": "%s", "remark": "%s"}""" % (resource, currentValue, threshold, remark)
        # aliyunsms.content = """ {"resource": "%s", "currentValue":"%s", "threshold": "%s", "remark": ""}""" % (resource, currentValue, threshold)
        aliyunsms.content = """ {"res":"%s", "cv":"%s", "sh":"%s", "rm":"%s"}""" % (resource, currentValue, threshold, remark)
        # aliyunsms.content =  """ {"resource": "%s", "detail": "%s", "remark":""}""" % (resource,detail)
        print(aliyunsms.content)
        print(len(aliyunsms.content))
        aliyunsms.aliyunSMS()

