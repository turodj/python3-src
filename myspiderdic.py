# -*- coding: UTF-8 -*

# 对bt蚂蚁（btmayi.me）网址进行爬取，usage： mayispider.py <查询关键字> <起始页数> <结束页数>

from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import OrderedDict
import socket,sys
import re
import urllib.request
import urllib
import sys,time

socket.setdefaulttimeout(120) #访问超时设为120秒



#定义获取电影名称和链接的函数
def get_magres(input_url):
		#伪装成为正常访问
		req=urllib.request.Request(input_url,headers= 
			{'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64;rv:23.0) Gecko/20100101 Firefox/23.0'})	
		#打开页面
		r1 = urllib.request.urlopen(req)
		soup1= BeautifulSoup(r1.read(),"html.parser")
		print (soup1.title)
		#print(soup1.prettify()) #输出整个页面
		[script.extract() for script in soup1.find_all('script')] #移除sript脚本
		#输出一个完整文档
		#fp=open("/Users/dongjian/spiderdoc/testhtml.html","w")
		#fp.write(soup1.prettify())
		#fp.close()

		
		avnamelist=[]
		avlinklist=[]
		avinfoall=[]
		#find  av的所有信息
		avinfoall =soup1.find_all("div",{"class":"search-item"})

		for avinfo in avinfoall:
			avtitle=avinfo.find("div",class_="item-title")
			avtitlestr=avtitle.get_text(strip=True) #获得去空格的文字内容
			avnamelist.append(avtitlestr)
			#print("name = %s"%avtitlestr)
			#取av 磁力链接
			avmag=avinfo.find("a",href=re.compile(r'^(\s)*magnet'))
			avlink=avmag.get("href")
			avlinklist.append(avlink)
			#print("link = %s"%avlink)

		return avnamelist,avlinklist #函数结束，返回av名称，av链接



#程序正文开始
#对中文查询条件进行转译
snametemp=sys.argv[1] #通过参数传递查询条件
sname=urllib.parse.quote(snametemp) #中文参数标准化编码

beginpage=int(sys.argv[2]) # 开始页数
endpage=int(sys.argv[3])  #结束页数

#准备好写入的文件
basepath="/Users/dongjian/spiderdoc/"
finename=basepath+sys.argv[1]+".txt" #第一个参数形成文件名
targetfile=open(finename,"a")

page=endpage #从尾页开始搜索
getavlist=[]
getavmaglist=[]
avlist=[]
searchedpage=0
avdict=OrderedDict()
#循环搜索每页
while page >= beginpage :
	
	url="http://www.btmayi.me/search/%s-size-asc-%d"%(sname,page) #搜索第page页
	print("begin search %s\n"%url)

	getavlist.clear()
	getavmaglist.clear()
	avlist.clear()
	avdict.clear()

	getavlist,getavmaglist=get_magres(url) #调用获取资源函数，返回av名称，av链接

	print("avres=%d,avmag=%d"%(len(getavlist),len(getavmaglist)))
	targetfile.write("\nsearch： url:%s\n\n"%url)
	#print(getavlist)
	#print(getavmaglist)
	#写入每个影片对应的链接
	
	avdict=OrderedDict(zip(getavlist,getavmaglist)) #形成有序字典，并同时剃重
	#写入av及对应的下载链接
	for key in avdict.keys():
		targetfile.write("%s|%s\n"%(key,avdict[key]))
		
	targetfile.write("--------maglink list-------\n")
	#逐行写入链接，每5行空一行
	#print("write %d magnet"%len(getavmaglist))
	avsum=0
	for key in avdict.keys():
		targetfile.write("%s\n"%avdict[key])
		avsum += 1
		if avsum%5 == 0 :
			targetfile.write("\n")
	
	targetfile.flush() #将缓存内容刷新到文件中
	

	page -= 1
	searchedpage += 1

	print(".......sleep 1 sec......")
	time.sleep(1) #休眠1秒，防止网站封ip
else:
	print("共查询了 %d 页"%searchedpage)

targetfile.close
print("get link over")

		