#coding=utf-8
import os
curdir = os.path.dirname(__file__)
import sys
sys.path.append(curdir) 
import os,web
import math
import thread
from time import ctime,sleep
from model import *
from sendemail import *
from white import *
from black import *
from similarity import *
from verifycode import *
from getdomainbyurl import *

web.config.debug = False

urls = (
    '/', 'index',
    '/index','index',
    '/check','check',
    '/report','report',
    '/verify','verify',
    '/register','register',
    '/login','login',
    '/logout','logout',
    '/forgetpasswd','forgetpasswd',
    '/admin','admin',
    '/help','help'
    )

t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}
render = web.template.render(os.path.join(curdir,'templates'), base='base', globals=t_globals)
app = web.application(urls, locals())
sess = web.session.Session(app, web.session.DiskStore(os.path.join(curdir,'sessions')), initializer = {'username': None,'verifycode':None})

verify_type_unknown=0
verify_type_phishing=1
verify_type_not_phishing=2
verify_type_report=3
verify_type_host=4

class index:
    def GET(self):
	return render.index()

class check:
    def GET(self):
        raise web.seeother('index')
    def POST(self):
	search = web.input()
	url = search.get('url')
	if url == "" or url ==None:
	    return render.message("checkerr") 
	url = url.strip()
	d = SLD()
	host = d.get_second_level_domain(url)
	if host=="" or host ==None:
	    return render.message("checkerr")
	print host
	m = Model()
	result = m.select_from_result_by_host(host)
	print result
	score_not_phishing = 0
	score_phishing = 0
	score_unknown = 0
	score_host_tag =0
 	for i in result:
	    if i[2] == verify_type_not_phishing:
		s = Similarity()
		if url == i[1]:
		    score_not_phishing = 100
		    score_phishing = 0
        	    score_unknown = 0
		    break
	 	elif s.similarity(url,i[1]) == True:	
		    score_not_phishing+=25
	    elif i[2] == verify_type_phishing:
	        s = Similarity()
                if url == i[1]:
                    score_not_phishing = 0
		    score_phishing = 100
        	    score_unknown = 0
		    break
		elif s.similarity(url,i[1]) == True:
                    score_phishing+=25
	    elif i[2] == verify_type_host and host == i[1]:
		if score_host_tag == 0:
		    score_host_tag =1
		    score_not_phishing=75+((len(host)*100)/(len(host)+len(url)))
		    score_phishing=0
		    score_unknown=0
	    elif i[2] == verify_type_report and url == i[1]:
	        verify=m.select_from_verify_by_resultid(i[0])
		for i in verify:
                    if i[1] == verify_type_phishing:
                        score_phishing+=25
                    elif i[1] == verify_type_not_phishing:
                        score_not_phishing+=25
        
        print score_not_phishing,score_phishing,score_unknown
	if score_not_phishing == 0 and score_phishing ==0 and score_unknown ==0:
            return render.message("checkerr")
	score_all = score_not_phishing+score_phishing
	if score_all >100:
	    score_not_phishing = (score_not_phishing*100)/score_all
	    score_phishing = (score_phishing*100)/score_all
	score_unknown = 100-score_not_phishing-score_phishing
	return render.check(score_not_phishing , score_phishing , score_unknown)

class report:
    def GET(self):
	vc = Verifycode()
        sess.verifycode = vc.getcode()
        return render.report()
    def POST(self):
	search = web.input()
        print search
        url = search.get('url')
	url = url.strip()
	verifycode = search.get('verifycode')
        print verifycode.lower() , sess.verifycode.lower()
        if verifycode.lower() != sess.verifycode.lower():
            print "report verifycode err"
	    return render.message("reporterr-verify")

	print sess.username
        m = Model()
	username = sess.username
	if username == None:
	    username = m.admin
	sp = Spider(url)
	if 1:
	#if sp.get_rescode == 200 and sp.get_html!=None:	
	    if False == m.insert_into_result(url, verify_type_report ,username):
	        print "report insert into result err"
		return render.message("reporterr-url")	    
	    if sess.username == None:
	 	return render.message("reportnotloginok")
	    else:
		return render.message("reportloginok")
	return render.message("reporterr")

class verify:
    def GET(self):
	search = web.input()
	md5 = search.get('code')
        m = Model()
	if md5!=None:
	    username = m.select_username_from_user_by_md5(md5)
            if username != None:
	        print "...%s"%username
	        m.update_verify_from_user_by_username(username)
	        return render.message("isverifier")		
	print sess.username
	if sess.username !=None:
	   if None == m.select_verify_from_user_by_username(sess.username):
		usernamemd5 = m.get_md5_value(sess.username)
		print "http://11.11.22.33/verify?code=%s"%(usernamemd5)	
		#se = Sendemail()
            	#se.sendemail(i)
		return render.message("notverifier")
	   result_verifying = m.select_from_result_for_verify(sess.username,verify_type_report)
           return render.verify(result_verifying) 
	else:
	    return render.login()
    def POST(self):
        search = web.input()
        print search 
	phishing = search.get('phishing')
        not_phishing = search.get('not_phishing')
	unknown = search.get('unknown')
	m = Model()
	verify_type=verify_type_unknown
	if phishing != None:
	    verify_type=verify_type_phishing
	    url = phishing
	elif not_phishing != None:
            verify_type=verify_type_not_phishing
	    url = not_phishing
        elif unknown != None:
            verify_type=verify_type_unknown
            url = unknown
	else:
	    raise web.seeother("/verify")	
	m.insert_into_verify(verify_type,sess.username,url)
	raise web.seeother("/verify")

class register:
    def GET(self):
	vc = Verifycode()
	sess.verifycode = vc.getcode()
	return render.register()
    def POST(self):
	search = web.input()
        username = search.get('username')
	passwd1 = search.get('password1')
	passwd2 = search.get('password2')
	verifycode = search.get('verifycode')
	if passwd1 != passwd2:
	    return render.message("registererr-passwd")
	print verifycode.lower() , sess.verifycode.lower()
	if verifycode.lower() != sess.verifycode.lower():
	    return render.message("registererr-verify")
        m = Model()
	if m.select_userid_from_user_by_username(username) != None:
	    return render.message("registererr-username")
        m.insert_into_user(username,passwd1)
        return render.message("registerok")

class login:
    def GET(self):
	return render.login()
    def POST(self):
	search = web.input()
	username = search.get('username')
	passwd = search.get('password')
	m = Model()
	result = m.select_rowcount_from_user_by_login(username,passwd)		
	if result ==1:
	    sess.username=username
  	    print sess.username
	    web.setcookie('username', username)
	    raise web.seeother('index')
	return render.message("loginerr")

class logout:
    def GET(self):
	#print sess.username
	sess.username=None
	sess.kill()
	web.setcookie('username', '', expires=-1)
	raise web.seeother('index')

class forgetpasswd:
    def GET(self):
	vc = Verifycode()
	sess.verifycode = vc.getcode()
        return render.forgetpasswd()
    def POST(self):
        search = web.input()
        username = search.get('username')
	verifycode = search.get('verifycode')
        print verifycode.lower() , sess.verifycode.lower()
        if verifycode.lower() != sess.verifycode.lower():
            return render.message("findpasswderr")
	m = Model()
	if m.select_userid_from_user_by_username(username) == None:
	    return render.message("findpasswderr") 
        #se = Sendemail()
        #se.sendemail(username , "密码test")
	return render.message("findpasswd")

class help:
    def GET(self):
        m = Model()
        result = m.select_from_result_by_verify_type_for_show(verify_type_phishing)
        return render.help(result)
class admin:
    def GET(self):
	m = Model()
	user = m.select_from_user_for_admin()
	result = m.select_from_result_for_admin()
	verify = m.select_from_verify_for_admin()
	count = []
	user_count = m.select_rowcount_from_user()
	count.append(user_count)
	result_count_verify_type_not_phishing = m.select_rowcount_from_result(verify_type_not_phishing)
	count.append(result_count_verify_type_not_phishing)	
	result_count_verify_type_phishing = m.select_rowcount_from_result(verify_type_phishing)
	count.append(result_count_verify_type_phishing)
	result_count_verify_type_report = m.select_rowcount_from_result(verify_type_report)
	count.append(result_count_verify_type_report)
	result_count_verify_type_host = m.select_rowcount_from_result(verify_type_host)
        count.append(result_count_verify_type_host)
        return render.admin(user , result , verify ,count)
    def POST(self):
        search = web.input()
        btn = search.get('btn')
        m = Model()
        if btn == "white":
	    d = SLD()
	    ws = WhiteSpider()
	    result = ws.get_all_result()
            for i in result:
                print "%s\n////////////"%i
		host = d.get_second_level_domain(i)
		print host
        	if host!="" and host!=None:
                    m.insert_into_result(host, verify_type_host ,m.admin)
        elif btn == "black":
	    bs = BlackSpider()
	    result = bs.phishtank()
	    for i in result:
	        #print "%s\n////////////"%i
         	m.insert_into_result(i, verify_type_phishing ,m.admin)
	elif btn == "sendemail":
            se = Sendemail()
            result = m.select_from_user_for_sendemail()
            for i in result:
		print i[1]
	        #se.sendemail(i[1])
	        #m.del_from_sendemail(sess.username)
		#m.insert_into_sendemail(i[0])
        elif btn == "similarity":
	    s = Similarity()
	    result_report = m.select_from_result_for_verify(m.admin, verify_type_report)
	    result_not_phishing = m.select_from_result_by_verify_type(verify_type_not_phishing)
	    print result_report
	    for i in result_report:
	        for j in result_not_phishing:
		    print i[1],j[1]
		    #if s.similarity(i[1] , j[1]) ==True:
		    #    m.insert_into_verify(verify_type_phishing,m.admin,i[1])
		    #else:
		    #    m.insert_into_verify(verify_type_not_phishing,m.admin,i[1])
        else:
	    raise web.seeother("/admin")	
	raise web.seeother("/admin")

if not __name__ == "__main__":    
    application = app.wsgifunc()
else:
    app.run()
	
