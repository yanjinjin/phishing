# encoding: UTF-8
import urllib2
import re
import os
import string
import socket

class Spider(object):
    def __init__(self,url):
	print "spider start"
	self.rescode = 0
	self.html = None
	self.result = []
	self.url = url
	self.res = None
	print "start connect...."
        try:
            socket.setdefaulttimeout(2)
            req = urllib2.Request(url)
	    req.add_header('Referer', 'http://tieba.baidu.com/')
            req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
	    self.res = urllib2.urlopen(req)
	    self.rescode = self.res.getcode()
	    self.html =  self.res.read()
	except urllib2.URLError, e:
	    self.html = None
	    print e.reason
	    print "connect failed"+url	
    
    def get_rescode(self):
	#200
	return self.recode

    def get_html(self):
	return self.html

    def parse_html(self):
	return self.result

    def __del__(self):
        print "spider over"
	if self.res!=None:
	    self.res.close()
	    del self.res
