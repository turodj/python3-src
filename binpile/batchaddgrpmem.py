# -*- coding: UTF-8 -*
#增加组成员，流程：1判断是是否是客户,是否已经是群成员了 2 是否有活跃组，当前组是否满了，如果满了进行分组操作  3 增加到给定的组中group_member表中 
#执行方法 python3 addgrpmemt.py <手机号>


import socket,sys,os
import re
import urllib
import sys,time,random
import pymysql


from binmysql import * #可以应用binmysql.py中的函数
from readgrpmem import *
from binpile import Binpile
from addgrpmem import *




if __name__ == "__main__":
	
	conn,cur=connDB()
	sql="select phone_no from cust_info where cust_id not in (select node_id from group_member  )"
	exeSelect(cur,sql)
	getdata=list(cur.fetchall())
	print(getdata)
	connClose(conn,cur)

	for x in range(50):
		tmp= random.choice(getdata)
		phone_no=tmp[0]

		sta,code,content=addgrpmem(phone_no)
		if sta == True and code == 2: # 分群成功，重新调用addgrpmem添加到新群
			addgrpmem(phone_no)
			#print(retcontent)
	

