from spider import *

class PhishtankBlackSpider(Spider):
    def parse_html(self):
        file = "download/%s"%(self.url[self.url.rindex('/')+1:])
        file = os.path.join(os.path.dirname(__file__),file)
        print file
	if self.get_rescode == 200 and self.get_html!=None:
            file_object = open(file , 'w+')
            try:
                file_object.write(self.get_html)
            finally:
                file_object.close()

	file_object = open(file, 'r')
	try:
	    #file_object.write(text)
	    text = file_object.readlines()
	    for line in text:
		column = line.split(',')
		self.result.append(column[1])	
	finally:
            file_object.close()
	
	return self.result

class BlackSpider:
    def phishtank(self):
        url = "http://data.phishtank.com/data/68b4c2263bc5687ad3f275f69de3dbba4ae5219aa88c349125d73a064260f866/online-valid.csv"
        print url
	s = PhishtankBlackSpider(url)
        result=s.parse_html()
        return result
