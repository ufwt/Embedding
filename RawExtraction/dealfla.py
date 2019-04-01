import numpy as np
import scipy.io as sio
from FEfun import FEfun
import time
import os
import scipy.io

def justify_fla(matrix):
	isfla=False
	num=len(matrix)
	sumone=0
	flagmax=0
	flagone=0
	for i in range(num):
		if sum(matrix[:,i])>0.3*num:
			flagmax=1
			break
	for i in range(num):
		if sum(matrix[:,i])==1:
			sumone=sumone+1
	if num-sumone==3 or num-sumone==4:
		flagone=1
	if flagmax==1 and flagone==1:
		isfla=True
	return isfla

def find_specialnode(matrix,block_feature):
	rr={}
	num=len(matrix)
	#i=0
	#matrix.tranpose()
	for i in range(num):
		if sum(matrix[:,i])==0:
			break
	startnode=i
	print startnode
	rr[0]=block_feature[startnode].tolist()
	maindispacher=np.argwhere(matrix[startnode,:]==1)[0][0]
	for y in np.argwhere(matrix[:,maindispacher]==1):
		print y
		#if y[0]!=startnode:
			#break
	for jj in range(len(y)):
		if y[jj]!=startnode:
			break
	yudispacher = y[jj]
	#trueblock = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,[],[]]
	k1 = 0
	trueblock = []
	for k1 in range(5):
		trueblock.append(0)
	#trueblock.append([])
	#trueblock.append([])
	length=len(trueblock)
	i = 0
	for i in range(num):
		if matrix[i,yudispacher]==1:
			j = 0
			print i
			#for j in range(length):
				#trueblock[j] = trueblock[j] + block_feature[i][j]
			rr[i]=block_feature[i]
		#if matrix[yudispacher,i]==1:
		#	rr[i]=block_feature[i]
	##for i in range(num):
		#if sum(matrix[i,:])==0:
		#	break
	#startnode=i
	#returnblock = i
	#rr[2]=block_feature[returnblock].tolist()
	return rr
path='network/'
files= os.listdir(path)
s = []
for file in files:
	print(file)
	if not os.path.isdir(file):
		GG = sio.loadmat(path + file)
        G = GG["network"]
        G_name = os.path.basename(path + file)
        A_name = 'node' + G_name[4:]
        AA = sio.loadmat('attt/' + A_name)
        A = AA["network"]
	if justify_fla(G):
		Anew=find_specialnode(G,A)
		#print file
        #print Anew
	#j=0
	network=[]
	for i in Anew.values():
		network.append(i)
		#j=j+1
	print network
	scipy.io.savemat('att/' + str(A_name) + '.mat', mdict={'network': network})

