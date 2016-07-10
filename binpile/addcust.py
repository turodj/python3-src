# -*- coding: UTF-8 -*
#执行方法 python3 addcust.py <姓名> <手机号> <金额>


import socket,sys,os
import re
import urllib
import sys,time
import pymysql

from binpile import Binpile
from binmysql import * #可以应用binmysql.py中的函数


def addcust(cust_name,phone_no,money): #cust_id 自增，不用显性插入
	conn,cur = connDB()
	addsql="insert cust_info(cust_name,phone_no,money) values('%s','%s',%d)"%(cust_name,phone_no,int(money)) 

	print(addsql)

	try:
		stat=exeInsert(cur,addsql)
	except pymysql.err.InternalError as e:
		print("mysql error",e)
		cur.execute("rollback")
	else:
		print("commit")
		cur.execute("commit")
		
	
	#stat=exeInsert(cur,addsql)
	#if stat == 1:
	#	print("sucess")
	#	cur.execute("commit")
	#else:
	#	print("fail")
	#	cur.execute("rollback")
#


	connClose(conn,cur)

if __name__ == "__main__":
	cust_name=sys.argv[1]
	phone_no=sys.argv[2]
	money=sys.argv[3]
	print(cust_name,phone_no,money,type(money),getnowtime())
	
	addcust(cust_name,phone_no,money)
	
	

	
