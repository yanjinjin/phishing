from spider import *
from spider_proxy import *
import os

class PhishtankBlackSpider(spider_parse):
    def __init__(self):
	file = "download/black/"
        dir = os.path.join(os.path.dirname(__file__),file)
	self.real_dir = os.path.join(dir , "data-phishtank-com")
	proxys = getProxys()
	s=Spider("http://data.phishtank.com/data/68b4c2263bc5687ad3f275f69de3dbba4ae5219aa88c349125d73a064260f866/online-valid.csv", proxys , dir)
        s.set_white("\.csv")
	s.run()
    
    def parse_data(self):
	result=[]
	filelist=[]
	self.get_all_file(self.real_dir,filelist)
	for file in filelist:
	    print file
	    file_object = open(file, 'r')
            try:
                text = file_object.readlines()
	        for line in text:
		    column = line.split(',')
		    result.append(column[1])
	    except:
                continue
	    finally:
            	file_object.close()
	return result 


class BlackSpider:
    def get_all_result(self):
        s = PhishtankBlackSpider()
        result=s.parse_data()
        return result
