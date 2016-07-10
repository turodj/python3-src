# -*- coding: UTF-8 -*

import socket,sys,os
import re
import urllib
import sys,time

from binpile import Binpile


def main():
	
	basepath="/Users/dongjian/groupdata"
	ginfoname="group_info"
	binpilefile="/binpile_info.csv"
	
	linelist=[]
	openfilename=basepath+binpilefile
	groupinfo=[]
	#g,node,parent,flag=0
	

	#打开文件，并把文件内容存入列表
	fp=open(openfilename,"r",encoding="utf-8")
	for i in fp.readlines():
		linelist.append(i)

	groupinfo=linelist.pop(0) #第一行是组信息，建立组
	g,node,parent,flag=groupinfo.strip().split(",")
	grouparry=Binpile(node) #根据群主建群

	nodelist=[]
	for x in linelist:
		
		g,node,parent,flag=x.strip().split(",")
		#print(node,type(node))
		nodelist.append(node)
	
	

	grouparry.bappend(nodelist)
	tmplist=grouparry.show_delta()
	
	for t in tmplist:
		print(t)
	fp.close()



if __name__=='__main__':
	main()
			



