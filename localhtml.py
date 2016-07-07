# -*- coding: UTF-8 -*

from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import OrderedDict
import re

#回文判断
def t_re(x):
	s=str(x)
	l=len(s)
	i=0
	while s[i]==s[-i-1] and i<(l-1)/2 :
		#print("number %d"%i,s[i],s[-i-1])
		i=i+1
	if s[i]==s[-i-1] :#如果符合条件的最后一个字符扔相等说明是回文
		 return(1)
	else: 
		return(0)	
#回文判断方式2
def t_rec2(x):
	s=str(x)
	z=''.join(list(reversed(s))) #通过reversed进行字符串反转
	if s == z :
		return(1)
	else:
		return(0)


	


#r1 = urlopen("http://www.si-tech.com.cn")
r1=open("/Users/dongjian/spiderdoc/testhtml.html","rb")
r2=open("/Users/dongjian/spiderdoc/test.txt","w",encoding="utf-8")

soup1= BeautifulSoup(r1.read(),"html.parser")
print (soup1.title)
#print(soup1.prettify())
avnamelist=[]
avlinklist=[]


avinfoall=soup1.find_all("div",{"class":"search-item"})

for avinfo in avinfoall:
	#取av名字
	avtitle=avinfo.find("div",class_="item-list")
	avtitlestr=avtitle.get_text(strip=True) #获得去空格的文字内容
	avnamelist.append(avtitlestr)
	print("name = %s"%avtitlestr)
	#取av 磁力链接
	avmag=avinfo.find("a",href=re.compile(r'^(\s)*magnet'))
	avlink=avmag.get("href")
	avlinklist.append(avlink)
	#print("link = %s"%avlink)

avdict=OrderedDict(zip(avnamelist,avlinklist)) #形成有序字典，并同时剃重
for key in avdict.keys():
	r2.write("%s|%s\n"%(key,avdict[key]))	
	if key.find("中文字幕")>=0 :
		print("%s|%s"%(key,avdict[key]))

avsum=0
r2.write("=="*10+"\n")
for key in avdict.keys():
	r2.write("%s\n"%avdict[key])
	avsum+=1
	if avsum%5 == 0:
		r2.write("\n")
			
r1.close()
r2.close()




	
	