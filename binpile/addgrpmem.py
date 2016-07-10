# -*- coding: UTF-8 -*
#增加组成员，流程：1判断是是否是客户,是否已经是群成员了 2 是否有活跃组，当前组是否满了，如果满了进行分组操作  3 增加到给定的组中group_member表中 
#执行方法 python3 addgrpmemt.py <手机号>


import socket,sys,os
import re
import urllib
import sys,time
import pymysql


from binmysql import * #可以应用binmysql.py中的函数
from readgrpmem import *
from binpile import Binpile


def iscust(cur,phone_no): #判断是否是客户
	qrysql="select cust_id from cust_info where phone_no = '%s'"%(phone_no)
	exeSelect(cur,qrysql)
	

def ismember(cur,cust_id): #判断是否是成员
	qrysql="select *  from  group_member where node_id = %d "%(cust_id)
	exeSelect(cur,qrysql)
	

def getmem(cur): #获取活跃群成员,按先后顺序
	qrysql="select b.* from group_info a,group_member b where a.group_id =b.group_id and a.live_flag='1' order by seq"
	exeSelect(cur,qrysql)
	

def addgrp(cur,cust_id,phone_no): #创建组，并将cust_id 设为群主，插入group_info,group_member
	
	#insert group_info
	insgrpsql="insert group_info(group_master,group_name,live_flag) values(%d,%s,'1')"%(cust_id,phone_no)
	sta=exeInsert(cur,insgrpsql)
	#print(insgrpsql,'\nins sta=',sta)
	if sta!=1 :
		return(False)
	
	#insert group_member
	insmemsql="insert group_member(group_id,node_id,parent_id,left_flag,right_flag) select a.group_id,%d,0,'0','0' from group_info a where group_master=%d"%(cust_id,cust_id)
	sta=exeInsert(cur,insmemsql)
	#print(insmemsql,'\nins sta=',sta)
	if sta!=1:
		return(False)

def divgrp():
	pass

def updategrand(cur,group_id,node_id):#更新节点上溯祖先的余额
	grparry=readgrpmem(cur,group_id) #获取二叉树
	grandlist=grparry.get_grand(str(node_id))  #获取其祖先节点
	addmoney=200
	for node in grandlist:
		updsql="update cust_info set money=money+%d where cust_id = %d"%(addmoney,int(node.key))
		sta=exeUpdate(cur,updsql)
		print('update cust_id ',node.key)
		if sta!=1 :
			return(False)
	else:
		return(True)

	

def insmem(cur,memdata,cust_id): #添加成员记录，添加父子关系，先left键，后right建,触发更新其所有祖先的金额

	for record in memdata:#循环变量取得的记录
		seq,group_id,node_id,parent_id,left_flag,right_flag=record # 将元组记录中的各个字段赋给变量
		if  left_flag=='0' or right_flag=='0' :  # 判断二叉树有空余分支
			break #跳出循环
	else: #没有空余的二叉树，返回
		return(False)

	print(record)
	#根据获得分支记录，更新此记录
	if left_flag == '0':
		upsql="update group_member set left_flag='1' where seq=%d"%(seq)
	elif right_flag == '0' :
		upsql="update group_member set right_flag='1' where seq=%d"%(seq)
	else:
		return(False)
	
	sta = exeUpdate(cur,upsql)
	print("update = ",upsql,"\nstat= ",sta)
	if sta!=1:
		return(False)
	
	# 插入新增子节点,更新父子关系
	insmemsql="insert group_member(group_id,node_id,parent_id,left_flag,right_flag) values(%d,%d,%d,'0','0')"%(group_id,cust_id,node_id)
	sta=exeInsert(cur,insmemsql)
	
	print(insmemsql,'\nins sta=',sta)
	if sta!=1:
		return(False)

	# 更新此新增节点所有祖先的金额
	if updategrand(cur,group_id,cust_id) == False:
		return(False)
	


def addgrpmem(phone_no): #增加成员到某组
	conn,cur = connDB()
	
	iscust(cur,phone_no) #判断是否是客户，如果是获取其cust_id
	if cur.rowcount!=1 :
		print(phone_no ,"is not cust,or phone is not only")
		return(False)
	
	getdata=cur.fetchone()
	cust_id=getdata[0]
	print(cust_id)

	ismember(cur,cust_id) #判断是否是已经是成员,已是成员不能再加入
	
	if cur.rowcount!=0 :
		print(phone_no,cust_id ,"already is member ")
		return(False)

	getmem(cur) #获取当前活跃群组，返回结果集。分3钟情况 1.记录数0，说明没有活跃群，创建群组，并插入群成员中；2.记录数》max最大成员数 分群 3.<小于最大成员数，添加记录，更新父子关系
	
	print("mem count",cur.rowcount)
	if cur.rowcount == 0: #1.记录数0，说明没有活跃群，创建群组，并插入群成员中；
		
		cur.execute("start transaction")
		if addgrp(cur,cust_id,phone_no) != False:
			cur.execute("commit")
		else:
			cur.execute("rollback")
	
	elif cur.rowcount == 63-1:#如果等于分群条件，一个群最大数量为63人，则分群
		
		getdata=cur.fetchone()
		grp_id=str(getdata[1])
		cur.execute("start transaction")
		if divgrp(cur,grp_id) != False:
			cur.execute("commit")
		else:
			cur.execute("rollback")
	
	else: #以上都不是，增加到组中，更新组中的父子关系
		memdata=cur.fetchall() # 获取群组成员
		cur.execute("start transaction")
		if insmem(cur,memdata,cust_id) != False:
			cur.execute("commit")
		else:
			cur.execute("rollback")




	connClose(conn,cur)

if __name__ == "__main__":
	
	phone_no=sys.argv[1]
	print(phone_no)
	
	addgrpmem(phone_no)
