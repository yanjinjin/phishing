#!/usr/bin/env python
#coding=utf8

import urllib2
import json
import hashlib
import time

WEIXIN_TOKEN = '111111'
WEIXIN_APPID = 'wx7728db155e6b6e20'
WEIXIN_SECRET = '5bb0be1f8414b83bd14b6f22e6a2da94'
WEIXIN_URL = 'http://phishfeeds.com'

class index_weixin():
    def get_access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        WEIXIN_APPID,WEIXIN_SECRET)
        result = urllib2.urlopen(url).read()
        weixin_access_token = json.loads(result).get('access_token')
        print 'access_token===%s' % weixin_access_token
 	return weixin_access_token
  
    def get(self,signature,timeStamp,nonce,echostr):
        token=WEIXIN_TOKEN
        tmp = [token, timeStamp, nonce]
        tmp.sort()
        raw = ''.join(tmp).encode()
        sha1Str = hashlib.sha1(raw).hexdigest()
        print sha1Str
        print signature
	if sha1Str == signature:
            return echostr
	else:
	    return None
