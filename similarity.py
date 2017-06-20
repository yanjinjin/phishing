#coding=utf-8
import math
from ctypes import *
import os

LEVENSHTEIN_SO = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),"Levenshtein/Levenshtein.so"))

class Similarity:
    def __init__(self):
	self.L_DOUBLE = LEVENSHTEIN_SO.lev_u_jaro_ratio
	self.L_DOUBLE.restype = c_double

    def similarity(self,str1,str2):
        jaro_ratio = self.L_DOUBLE(len(str1),str1,len(str2),str2)
        distance = LEVENSHTEIN_SO.lev_u_edit_distance(len(str1),str1,len(str2),str2,0)
        print jaro_ratio
        print (distance*100)/(distance+(len(str1)+len(str2))/2)
        if(jaro_ratio >= 0.85 and (distance*100)/(distance+(len(str1)+len(str2))/2) <=10):
            return True
        return False
