# coding=utf-8
from bp import *
from spider import *

class Phishingbp(Spider_one):
    def __init__(self):
	#https,form,icp
        pat = [
            [[0,0,0], [0]],
            [[0,0,1], [0]],
	    [[0,1,0], [0.9]],
	    [[1,0,0], [0]],
            [[0,1,1], [0.2]],
            [[1,0,1], [0]],
	    [[1,1,0], [0.5]],
            [[1,1,1], [0]]
        ]

        # create a network with three input, two hidden, and one output nodes
        n = NN(3, 2, 1)
        # train it with some patterns
        n.train(pat)
    	self.pn = n

    def get_html(self,url):
	s = Spider_one(url)
        if s == None:
	    return None
	result=s.parse_html()
        return result

    def parse_html(self,url):
        result=[0,0,0]
        filelist=[]
	print url
	if url[0:8] == 'https://':
	    result[0] = 1
        c = self.get_html(url)
	if c==None or c == []:
	    return result
	c=c.lower()
        if c.find("icp")!=-1 or c.find("备")!=-1:
            result[2] = 1

	form_start = c.find("<form")
        if form_start != -1:
            form_end = c.find("</form")
            if form_end != -1:
                c = c[form_start:form_end]
		print "input count:%d,type hidden %d"%(c.count("<input "),c.count("<input type=\"hidden\""))
		input_num = c.count("<input ") - c.count("<input type=\"hidden\"")
		if 2 <= input_num <= 6:
                    if c.find("submit")!=-1 or c.find("<button")!=-1 or c.find("登 录")!=-1 or c.find("登录")!=-1 or c.find("user")!=-1 or c.find("login")!=-1 or c.find("账号")!=-1 or c.find("用户")!=-1 or c.find("passwd")!=-1 or c.find("password")!=-1 or c.find("密码")!=-1:
	    		result[1] = 1
        return result

    def predict(self , url):
	result = self.parse_html(url)
        return int(100*self.pn.predict(result)[0])

