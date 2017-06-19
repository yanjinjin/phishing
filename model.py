#coding=utf-8
import os,web,time,datetime
import sqlite3 as db
import math
import hashlib

class Model:
    def __init__(self):
	self.db = "phishing.db"
	self.table_user="user"
	self.table_sendemail="sendemail"
	self.table_result = "result"
	self.table_verify ="verify"
	self.admin = "admin@admin"
        if os.path.exists(self.db):
            self.conn = db.connect(self.db, check_same_thread=True)
        else:
            self.conn = db.connect(self.db, check_same_thread=True)
	    sql = "create table %s(id integer primary key,username text,passwd text, verifier int,date text,domain1 text,domain2 text) "%(self.table_user)
            self.conn.execute(""+sql+"")
            print 'create db %s'%(self.table_user)
	    sql = "insert into %s (username,passwd,verifier,date) values ('%s', '%s', %d,'%s')"%(self.table_user, self.admin, "ymj!yzc@20131225", 1, datetime.datetime.now())
            print sql
	    self.conn.execute(""+sql+"")
            self.conn.commit()

	    sql = "create table %s(id integer primary key,userid int) "%(self.table_sendemail)
            self.conn.execute(""+sql+"")
            print 'create db %s'%(self.table_sendemail)

	    sql = "create table %s(id integer primary key, url text, userid int, verify_type int, whois text,html_data text, date text,domain1 text, domain2 text) "%(self.table_result)
            self.conn.execute(""+sql+"")
            print 'create db %s'%(self.table_result)

	    sql = "create table %s(id integer primary key,verify_type int, userid int,resultid int,date text) "%(self.table_verify)
            self.conn.execute(""+sql+"")
            print 'create db %s'%(self.table_verify)

        self.cu = self.conn.cursor()
    
    def get_md5_value(self, src):
	myMd5 = hashlib.md5()
	myMd5.update(src)
	myMd5_Digest = myMd5.hexdigest()
	return myMd5_Digest

    def select_from_user_for_admin(self):
	sql = "select id , username, date from %s order by date DESC"%(self.table_user)
	self.cu.execute(""+sql+"")
	return self.cu.fetchall()

    def select_username_from_user_by_md5(self,md5):
        sql = "select username from %s"%(self.table_user)
        self.cu.execute(""+sql+"")
        res = self.cu.fetchall()
        for i in res:
           if md5 == self.get_md5_value(i[0]):
		return i[0]
	return None

    def select_verify_from_user_by_username(self,username):
        sql = "select id from %s where username ='%s' and verifier =1 limit 1"%(self.table_user,username)
	self.cu.execute("select id from user where username =? and verifier =? limit 1" , (username,1))
        res = self.cu.fetchall()
	for i in res:
            return i[0]
        return None

    def select_rowcount_from_user_by_login(self,username,passwd):
	sql = "select id from %s where username ='%s' and passwd = '%s'"%(self.table_user,username,passwd)
	print sql
	self.cu.execute("select id from user where username =? and passwd = ?",(username,passwd))
        res = self.cu.fetchall()
        rowcount=0
        for i in res:
            rowcount = rowcount + 1
        return rowcount
    
    def select_rowcount_from_user(self):
        sql = "select id from %s"%(self.table_user)
        self.cu.execute(""+sql+"")
        res = self.cu.fetchall()
        rowcount=0
        for i in res:
            rowcount = rowcount + 1
        return rowcount

    def select_userid_from_user_by_username(self,username):
	sql = "select id from %s where username ='%s' limit 1"%(self.table_user,username)
        self.cu.execute("select id from user where username =? limit 1" , (username,))
        res = self.cu.fetchall()
	for i in res:
	    return i[0]
	return None

    def insert_into_user(self,username,passwd):
	sql = "insert into %s (username,passwd,verifier,date) values ('%s', '%s', %d, '%s')"%(self.table_user, username, passwd, 0,datetime.datetime.now())
    	print sql
        self.conn.execute("insert into user (username,passwd,verifier,date) values (?, ?, ?, ?)" , (username, passwd, 0,datetime.datetime.now()))
        self.conn.commit()	
			
    def update_verify_from_user_by_username(self,username): 
	sql = "update %s set verifier = 1 where username = '%s'"%(self.table_user,username)
        print sql
        self.conn.execute("update user set verifier = ? where username = ?" ,(1,username))
        self.conn.commit()	
	
    def select_from_user_for_sendemail(self):
        sql = "select * from %s where id not in (select userid from %s)"%(self.table_user,self.table_sendemail)
        self.cu.execute(""+sql+"")
        return self.cu.fetchall()

    def insert_into_sendemail(self,userid):
	sql = "insert into %s (userid) values (%d)"%(self.table_sendemail, userid)
        self.conn.execute(""+sql+"")
        self.conn.commit()		
    
    def del_from_sendemail(self,username):
	userid=self.select_userid_from_user_by_username(username)
        sql = "delete from %s where userid = %d"%(self.table_sendemail, userid)
        self.conn.execute(""+sql+"")
        self.conn.commit()		

    def select_rowcount_from_result(self,verify_type):
        sql = "select id from %s where verify_type =%d"%(self.table_result,verify_type)
        self.cu.execute(""+sql+"")
        res = self.cu.fetchall()
        rowcount=0
        for i in res:
            rowcount = rowcount + 1
        return rowcount

    def select_from_result_by_verify_type(self,verify_type):
	sql = "select * from %s where verify_type =%d limit 1"%(self.table_result, verify_type)
        self.cu.execute(""+sql+"")
        return self.cu.fetchall()	

    def select_from_result_by_verify_type_for_show(self,verify_type):
        sql = "select url,date from %s where verify_type =%d order by date DESC limit 10"%(self.table_result, verify_type)
        self.cu.execute(""+sql+"")
        return self.cu.fetchall()

    def select_from_result_by_host(self,host):
        sql = "select id,url,verify_type from result where (url='%s') or (url like '%s') or (url like '%s')"%(host,"%"+host,"http://%"+host+"%")
        print sql
        self.cu.execute("select id,url,verify_type from result where (url=?) or (url like ?) or (url like ?)",(host,"%"+host,"http://%"+host+"%"))
        return self.cu.fetchall()

    def select_from_result_by_url(self,url):
	sql = "select * from %s where url = '%s' limit 1"%(self.table_result,url) 
	print sql
	self.cu.execute("select * from result where url = ? limit 1" , (url))       
        return self.cu.fetchall()
    
    def select_resultid_from_result_by_url(self,url):
	sql = "select id from %s where url = '%s' limit 1"%(self.table_result,url)
	print sql
        self.cu.execute("select id from result where url = ? limit 1" , (url,))
        res = self.cu.fetchall()
        for i in res:
	    return i[0]
        return None

    def select_from_result_for_verify(self,username , verify_type):
        userid = self.select_userid_from_user_by_username(username)
    	if userid ==None:
	    return []
        sql = "select * from %s where verify_type=%d and id not in (select resultid from %s where userid=%d) order by date DESC limit 10"%(self.table_result , verify_type, self.table_verify , userid)
        print sql
        self.cu.execute(""+sql+"")
        return self.cu.fetchall()

    def select_from_result_for_admin(self):
	sql = "select id , url , verify_type ,date from %s order by date DESC limit 100"%(self.table_result)
        self.cu.execute(""+sql+"")
        return self.cu.fetchall()
    
    def insert_into_result(self, url,verify_type, username):
	resultid = self.select_resultid_from_result_by_url(url)
	if resultid!=None:
	    return False
	userid = self.select_userid_from_user_by_username(username)
        if userid == None:
	    return False
	sql = "insert into %s (url, userid,verify_type, date) values ('%s', %d, %d,'%s')"%(self.table_result, url, userid, verify_type, datetime.datetime.now())
        print sql
        self.conn.execute("insert into result (url, userid,verify_type, date) values (?, ?, ?,?)" , (url, userid, verify_type, datetime.datetime.now()))
        self.conn.commit()
	return True
    
    def insert_into_verify(self,verify_type,username,url):
	userid = self.select_userid_from_user_by_username(username)
	if(userid == None):
	    return None
	resultid = self.select_resultid_from_result_by_url(url)
	if(resultid == None):
	    return None
	sql = "insert into %s ( verify_type,userid,resultid,date) values ( %d, %d, %d,'%s')"%(self.table_verify,verify_type,userid,resultid, datetime.datetime.now())
	print sql
        self.conn.execute(""+sql+"")
        self.conn.commit()
	
    def select_from_verify_by_resultid(self,resultid):
	sql = "select * from %s where resultid=%d"%(self.table_verify , resultid)
        self.cu.execute(""+sql+"")
        return self.cu.fetchall()	
    
    def select_from_verify_for_admin(self):
        sql = "select verify.id,result.url,user.username,verify.verify_type,verify.date  from verify,user,result where verify.userid = user.id and verify.resultid = result.id order by verify.date DESC limit 100"
        self.cu.execute(""+sql+"")
        return self.cu.fetchall()
 
    def __del__(self):
	print 'close db conn'
	self.cu.close()
        self.conn.close()

