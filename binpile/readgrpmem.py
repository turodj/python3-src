# -*- coding: UTF-8 -*
#  执行方式 python3  readgrpmem.py <组标识>

import socket,sys,os
import re
import urllib
import sys,time
import pymysql


from binmysql import * #可以应用binmysql.py中的函数
from binpile import Binpile


def readgrpmem(cur,grp_id):
	
	qrysql="select * from group_member where group_id = %d order by seq"%(int(grp_id))

	exeSelect(cur,qrysql)

	memdata=list(cur.fetchall())

	groupinfo=memdata.pop(0) #第一行是组信息，建立组
	#seq,g,node,parent,left_flag,right_flag=groupinfo
	masternode=str(groupinfo[2])

	grouparry=Binpile(masternode) #根据群主建群

	nodelist=[]
	for record in memdata:
		
		seq,g,node,parent,left_flag,right_flag=record
		#print(node,type(node))
		nodelist.append(str(node))
	
	

	grouparry.bappend(nodelist)

	#tmplist=grouparry.show_delta()
	#
	#for t in tmplist:
	#	print(t)
	return(grouparry)



if __name__=='__main__':
	grp_id=sys.argv[1]
	
	conn,cur = connDB()

	grouparry=readgrpmem(cur,grp_id)
	

	tmplist=grouparry.show_keydelta()
	
	for t in tmplist:
		print(t,type(t))

	connClose(conn,cur)


