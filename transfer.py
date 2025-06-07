import parselatlon
import kminhash
import random
import matplotlib.pyplot as plt
import os
from matplotlib import pyplot as plt
from PIL import Image
from pathlib import Path
N=parselatlon.N
MOD=kminhash.MOD
K=100

def paint(coordinate1,coordinate2,p,path):
	x_coords = [x for x, y in coordinate1]
	y_coords = [y for x, y in coordinate1]
	plt.plot(y_coords, x_coords, linestyle='--', color='red',label='pathA')
	x_coords = [x for x, y in coordinate2]
	y_coords = [y for x, y in coordinate2]
	plt.plot(y_coords, x_coords, linestyle='--', color='green',label='pathB')
	plt.xlabel('latitude')
	plt.ylabel('longitude')
	plt.title('similarity ='+str(p))
	plt.legend()

	plt.grid(True)
	plt.axis('equal') 
	plt.savefig(path)
	plt.close()
   
def read(path):
	return parselatlon.parseGpx(path)

def trans(coordinate):
	return parselatlon.trans(coordinate)

def getmin(coordinate,P):
	point=[]
	for item in coordinate:
		a=list(item)
		point.append((a[0]+N//2)*N+a[1]+N//2)
	return kminhash.evaluate(K,list(set(point)),P)
	
def evaluate(coordinatea,coordinateb,P):
	mina=getmin(coordinatea,P)
	minb=getmin(coordinateb,P)
	tt=list(set(mina+minb))
	tt.sort()
	ans=tt[:K]
	mina=set(mina)
	minb=set(minb)
	ans=set(ans)
	return (len(mina&minb&ans)/K)

def evaluateraw(coordinate1,coordinate2):
	coordinate3=trans(coordinate1)
	coordinate4=trans(coordinate2)
	P=[random.randint(1,MOD-1) for _ in range(K)]
	ans=evaluate(coordinate3,coordinate4,P)
	return ans

def evaluateraw2(coordinate1,coordinate2):
	coordinate3=set(trans(coordinate1))
	coordinate4=set(trans(coordinate2))
	
	ans=len(coordinate3&coordinate4)/len(coordinate3|coordinate4)
	return ans
	
def evaluatepath(path1,path2,path="my.png"):
	coordinate1=read(path1)
	coordinate2=read(path2)
	ans=evaluateraw(coordinate1,coordinate2)
	paint(coordinate1,coordinate2,ans,path)
	

	
def sortpath(coors,index, K):
	fin=[]
	for i in range(0,len(coors)):
		if i!=index:
			fin.append((evaluateraw(coors[i],coors[index]),coors[i]))
	fin.sort(reverse=True)
	cnt=0
	for i in range(0,len(fin)):
		item=list(fin[i])
		if item[0]==0 or i>=K:
			break
		paint(coors[index],item[1],item[0],'website/'+str(i+1)+".png")
		cnt+=1
	return cnt
		
def paintpath(coors,index,K):
	K=sortpath(coors,index, K)
	#current_dir=Path.cwd()
	html=""
	for i in range(1,K+1):
		html=html+"<img src=\""+str(i)+".png"+"\", width='33%'>\n"

	with open("website/index.html", "w", encoding="utf-8") as f:
		f.write(html)


