#!/usr/bin/env python3  
#coding: utf-8  
import smtplib  
from email.mime.text import MIMEText  
      
class Sendemail:
    def __init__(self):
	self.sender = 'jin_jin_yan@163.com'  
	self.smtpserver = 'smtp.163.com'  
	self.username = 'jin_jin_yan'  
	self.password = 'YJ?123456'  
      
	self.smtp = smtplib.SMTP()  
	self.smtp.connect(self.smtpserver)  
	self.smtp.login(self.username, self.password)  

    def sendemail(self,receiver,msg):
	self.msg ="<html><h1>%s</h1></html>"%(msg)
        self.mimemsg = MIMEText(self.msg,'html','utf-8')
        self.mimemsg['Subject'] = 'python email test'
	self.smtp.sendmail(self.sender, receiver, self.mimemsg.as_string())  

    def __del__(self):
	print "sendemail over"
	self.smtp.quit()  
