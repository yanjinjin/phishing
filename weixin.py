#!/usr/bin/env python
#coding=utf8

import urllib2
import json
import hashlib
import time

WEIXIN_TOKEN = '123321'
WEIXIN_APPID = 'wx26942ed464cbb444'
WEIXIN_SECRET = '917cd5d34143e3cd2a1b366228f27ae2'
WEIXIN_URL = 'http://phishfeeds.com'

class weixin_handle:
    def get_access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        WEIXIN_APPID,WEIXIN_SECRET)
        result = urllib2.urlopen(url).read()
        weixin_access_token = json.loads(result).get('access_token')
        print 'access_token===%s' % weixin_access_token
 	return weixin_access_token
    
    def get(self,signature,timeStamp,nonce,echostr):
	if timeStamp == None or nonce == None:
	   return None
	tmp = [WEIXIN_TOKEN, timeStamp, nonce]
        tmp.sort()
        raw = ''.join(tmp).encode()
        sha1Str = hashlib.sha1(raw).hexdigest()
        print sha1Str
        print signature
	if sha1Str == signature:
            return echostr
	else:
	    return None
