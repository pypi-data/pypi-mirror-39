import struct
import time
import numpy as np
from progressbar import *

def isList(value):
	if(isinstance(value,type([]))):
		return True
	if(isinstance(value,type(np.zeros((1,1))))):
		return True
	return False
 
def isSubList(List):
	if(not isinstance(List,type([]))):
		return False
	for i in range(len(List)):
		if(isinstance(List[i],type([])))	:	
			return True
		return False
def ReadData(fo,length,frequency,type_of_unit):
	arr = [0 for i in range(frequency)]
	for i in range(frequency):
		if(type_of_unit==">c"):
			arr[i]=struct.unpack(type_of_unit,fo.read(length))
		else:
			arr[i]=sum(struct.unpack(type_of_unit,fo.read(length)))
	return arr;
def MatrixToList(Matrix,count=0):
	remp = []
	for i in range(len(Matrix)):
		if(not isList(Matrix[i])):
			remp.append(Matrix[i])
			count+=1
		else:
			ar,ac=MatrixToList(Matrix[i])
			count+=ac
			remp.extend(ar)
	return remp,count


def ListToMatrix(List,Matrix,index=0):
	if(Matrix.size<len(List)&index<=0):
		return ["Matrix not enough Space."]
	for i in range(len(Matrix)):
		if(not isList(Matrix[i])):
			Matrix[i]=List[index]
			index+=1
		else:
			mm,ii = ListToMatrix(List,Matrix[i],index)
			index=ii
	return Matrix	,index
	


			