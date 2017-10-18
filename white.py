from spider import *
from spider_proxy import *
import os

class AlexaGlobalSpider(spider_parse):
    def __init__(self):
	file = "download/white/"
        dir = os.path.join(os.path.dirname(__file__),file)
	self.real_dir = os.path.join(dir , "alexa-chinaz-com")
	proxys = getProxys()
	s=Spider("http://alexa.chinaz.com/Global/index.html",proxys,dir)
        s.set_white("alexa\.chinaz\.com/Global/index")
        s.set_white("alexa\.chinaz\.com/Language/index")
        s.set_white("alexa\.chinaz\.com/Country/index")
        s.set_white("alexa\.chinaz\.com/Category/index")
	s.run()
    
    def parse_url(self,data):
	result=[]
	host = data
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
                result.append(host[:index_3])
	return result

class WhiteSpider:
    def get_all_result(self):
        s = AlexaGlobalSpider()
        result=s.parse_data()
        return result
