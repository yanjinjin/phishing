from spider import *

class AlexaGlobalSpider(Spider):
    def is_domain(self,url):
        pattern = re.compile(r'(?i)^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$')
        match = pattern.match(url)
        if match:
            return True
        else:
            return False

    def get_data(self):
	file = "./download/%s"%(self.url[self.url.rindex('/')+1:])
        print file
        html = None
        if self.get_rescode == 200 and self.get_html!=None:
            file_object = open(file , 'w+')
            try:
                file_object.write(self.get_html)
            finally:
                file_object.close()

        file_object = open(file, 'r')
        try:
            html = file_object.read()
        finally:
            file_object.close()
	return html

    def parse_html(self):
	host = self.get_data()
	while 1:
	    index_1 = host.find('<div class="righttxt"><h3><a href')
	    if index_1 == -1:
		break
	    host = host[index_1:]
	    index_2 = host.find('</a><span>')
	    if index_2 == -1:
                break
	    index_2+=len('</a><span>')
	    host = host[index_2:]
	    index_3 = host.find('</span>')
	    if index_3 == -1:
		break
	    print host[:index_3]
	    if self.is_domain(host[:index_3]):
	        self.result.append(host[:index_3])
	return self.result 

class AlexaChinaSpider(AlexaGlobalSpider):
    def parse_html(self):
	host = self.get_data()
	while 1:
	    index_1 = host.find('<div class="CentTxt"><h3 class="rightTxtHead"><a href')
	    print index_1
	    if index_1 == -1:
		break
	    host = host[index_1:]
	    index_2 = host.find('</a><span class="col-gray">')
	    if index_2 == -1:
                break
	    index_2+=len('</a><span class="col-gray">')
	    host = host[index_2:]
	    index_3 = host.find('</span>')
	    if index_3 == -1:
		break
	    print host[:index_3]
	    if self.is_domain(host[:index_3]):
	        self.result.append(host[:index_3])
	return self.result 

class Bank2345Spider(AlexaGlobalSpider):
    def parse_html(self):
	html = self.get_data()
	linkPattern = re.compile("href=\"(.+?)\"")
	self.result= linkPattern.findall(html)
	return self.result 

class WhiteSpider:
    def alexa_global(self):
        result = []
        i=1
        while i<=20:
            if i==1:
                url = "http://alexa.chinaz.com/Global/index.html"
            else:
                url = "http://alexa.chinaz.com/Global/index_%d.html"%i
            s = AlexaGlobalSpider(url)
            result+=s.parse_html()
	    #print i , url , result
	    i+=1
        return result
		
    def alexa_china(self):
        result = []
        i=1
        while i<=1839:
            if i==1:
                url = "http://alexa.chinaz.com/all/index.html"
            else:
                url = "http://alexa.chinaz.com/all/index_%d.html"%i
            s = AlexaChinaSpider(url)
            result+=s.parse_html()
	    #print i , url , result
	    i+=1
        return result	

    def bank_2345(self):
        result = []
	url = "http://www.2345.com/bank_df.htm"
	s = Bank2345Spider(url)
	result =s.parse_html()
	url = "http://www.2345.com/mail.htm"
        s = Bank2345Spider(url)
        result +=s.parse_html()
	url = "http://www.2345.com/gov.htm"
        s = Bank2345Spider(url)
        result +=s.parse_html()	
        url = "http://www.2345.com/corp.htm"
        s = Bank2345Spider(url)
        result +=s.parse_html()
	url = "http://www.2345.com/law.htm"
        s = Bank2345Spider(url)
        result +=s.parse_html()
	url = "http://buy.2345.com/shangjia"
        s = Bank2345Spider(url)
        result +=s.parse_html()
	url = "http://buy.2345.com/haitao"
        s = Bank2345Spider(url)
        result +=s.parse_html()
	url = "http://www.2345.com/love.htm"
        s = Bank2345Spider(url)
        result +=s.parse_html()
	return result	
		
    def get_all_result(self):
	result = []
	#result = self.alexa_global()
	#result += self.alexa_china()
	result+=self.bank_2345()
	return result
