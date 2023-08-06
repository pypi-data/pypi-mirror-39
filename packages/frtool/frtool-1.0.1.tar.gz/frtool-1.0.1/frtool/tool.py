import struct
import time
import os
import numpy as np
from progressbar import *

def islist(value):
	if(isinstance(value,type([]))):
		return True
	if(isinstance(value,type(np.zeros((1,1))))):
		return True
	return False
 
def isl(List):
	if(not isinstance(List,type([]))):
		return False
	for i in range(len(List)):
		if(isinstance(List[i],type([])))	:	
			return True
		return False
def rd(fo,length,frequency,type_of_unit):
	arr = [0 for i in range(frequency)]
	for i in range(frequency):
		if(type_of_unit==">c"):
			arr[i]=struct.unpack(type_of_unit,fo.read(length))
		else:
			arr[i]=sum(struct.unpack(type_of_unit,fo.read(length)))
	return arr;
def mtl(Matrix,count=0):
	remp = []
	for i in range(len(Matrix)):
		if(not islist(Matrix[i])):
			remp.append(Matrix[i])
			count+=1
		else:
			ar,ac=mtl(Matrix[i])
			count+=ac
			remp.extend(ar)
	return remp,count

def ltm(List,Matrix,index=0):
	if(Matrix.size<len(List)&index<=0):
		return ["Matrix not enough Space."]
	for i in range(len(Matrix)):
		if(not islist(Matrix[i])):
			Matrix[i]=List[index]
			index+=1
		else:
			mm,ii = ltm(List,Matrix[i],index)
			index=ii
	return Matrix	,index
	
def gfs(path,mask):
	files = os.listdir(path)
	filderFile = list(filter(lambda f: True in map(f.endswith,mask),files))
	return filderFile
			
			