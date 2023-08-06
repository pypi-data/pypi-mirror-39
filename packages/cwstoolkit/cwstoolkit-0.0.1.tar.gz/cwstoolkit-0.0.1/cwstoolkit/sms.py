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
from aliyunsdkcore.profile import region_provider


import urllib.parse
import configparser

class SMS():
    """
    @param: smsconfigfile:  sms.conf config file 
    @param: mobile
    @param: content
    @return: sendstatus

    ## warn
    {"resource": "CPU", "detail": "the detail of warning info", "remark": "could be empty"}
    ## recovery
    {"resource": "CPU", "currentValue": "3%", "remark": "could be empty"}
    """

    def __init__(self, smscofigfile, mobile, content):
        self.sms_config_file = smsconfigfile
        self.mobile = mobile
        self.content = content


    def _getYunpianConfig(self):
        config = configparser.ConfigParser()
        config.read(self.sms_config_file)
        return config['yunpiansms']['api_key']

    def _getAliyunConfig(self):
        config = configparser.ConfigParser()
        config.read(self.sms_config_file)
        aliyunsms = {}
        aliyunsms['access_keyid'] = config['aliyunsms']['access_keyid']
        aliyunsms['access_keysecret'] = config['aliyunsms']['access_keysecret']
        aliyunsms['template_code_warn'] = config['aliyunsms']['template_code_warn']
        aliyunsms['template_code_recovery'] = config['aliyunsms']['template_code_recovery']
        aliyunsms['sign_name'] = config['aliyunsms']['sign_name']
        return aliyunsms

 
    def yunpiansms(self, smstype='warn'):
        """
        云片短信发送
        内容模板：
        {"resource": "CPU", "detail": "the detail of warning info", "remark": "could be empty"}
        """
        msg = {}
        apikey = self._getYunpianConfig()
        client = YunpianClient(apikey)

        # mobile template id
        if smstype == 'warn':
            template_id =  2651642
        elif smstype == 'recovery':
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


    

    def aliyunSMS(self, smstype='warn'):
        """
        阿里云发送短信
        """
        msg = {} 

        REGION = "cn-hangzhou"
        PRODUCT_NAME = "Dysmsapi"
        DOMAIN = "dysmsapi.aliyuncs.com"

        aliyunconfig = _getAliyunConfig()
        access_keyid = aliyunconfig['access_keyid']
        access_keysecret = aliyunconfig['access_keyid']
        template_code_warn = aliyunconfig['template_code_warn']
        template_code_recovery = aliyunconfig['template_code_recovery']
        sign_name = aliyunconfig['sign_name']
        

        acs_client = AcsClient(access_keyid, access_keysecret, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
        smsRequest = SendSmsRequest.SendSmsRequest()
        smsRequest.set_SignName(sign_name) 

        if smstype == 'warn':
            template_code = template_code_warn
        elif smstype == 'recovery':
            template_code = template_code_recovery

        smsRequest.set_TemplateCode(template_code)
        
        smsRequest.set_TemplateParam(self.content)

        if len(self.mobile.split(',')) > 1:
            for number in self.mobile.split(','):
            smsRequest.set_PhoneNumbers(number)
            smsResponse = acs_client.do_action_with_exception(smsRequest)
        else:
            smsRequest.set_PhoneNumbers(self.mobile)
            smsResponse = acs_client.do_action_with_exception(smsRequest)

        if smsResponse['Message'] == 'OK':
            msg['status'] = 200
            msg['content'] = "send sucessfully!"
        else:
            msg['status'] = 500
            msg['content'] = "Sorry, send sms failed! Exception like: %s" % smsResponse.Message

        return msg 



