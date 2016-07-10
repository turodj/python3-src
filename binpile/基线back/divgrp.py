# -*- coding: UTF-8 -*
#  群组拆分函数，执行方式 python3  divgrp.py <组标识>

import socket,sys,os
import re
import urllib
import sys,time
import pymysql


from binmysql import * #可以应用binmysql.py中的函数
from readgrpmem import * # 用到readgrpmem.py中的函数
from binpile import Binpile

def credivgrp(cur,old_custid,lnew_custid,rnew_custid): #group_info表，移走老群名称，增加新分裂后的2个新群记录，先左后右，致序列最小的组为live组
	
	#插入历史表
	hissql="insert grpinfo_his (group_id,group_master,group_name,datatime) select group_id,group_master,group_name,'%s' from group_info where group_master=%d"%(getnowtime(),int(old_custid))
	exeInsert(cur,hissql)
	
	#删除当前group_info表
	delsql="delete from group_info where group_master=%d"%(int(old_custid))
	print("delte sql ==",delsql)
	exeDelete(cur,delsql)
	print("after delete")

	#插入左右两个记录
	lsql="insert group_info(group_master,group_name,live_flag) select cust_id,phone_no,'0' from cust_info where cust_id=%d"%(int(lnew_custid))
	exeInsert(cur,lsql)	
	rsql="insert group_info(group_master,group_name,live_flag) select cust_id,phone_no,'0' from cust_info where cust_id=%d"%(int(rnew_custid))
	exeInsert(cur,rsql)	

	#获最小的组号
	selsql="select group_id,group_master from group_info order by group_id"
	exeSelect(cur,selsql)
	mindata=cur.fetchone()
	mingrpid=mindata[0]

	lgrp_id=0
	rgrp_id=0
	#获取左右组号
	sqldata=cur.fetchall()
	for record in sqldata:
		grpid,grpmaster = record
		if grpmaster == int(lnew_custid):
			lgrp_id=grpid
		if grpmaster == int(rnew_custid):
			rgrp_id=grpid
		if lgrp_id!=0 and rgrp_id !=0 :
			break

	#更新全表中组号最小的组为活跃组
	updsql="update group_info set live_flag = '1' where group_id =%d "%(mingrpid)
	exeUpdate(cur,updsql)
	
	print("l,r new custid",lnew_custid,rnew_custid)
	print("new grp",lgrp_id,rgrp_id)
	return(lgrp_id,rgrp_id)



def popmaster(cur,old_custid):#推出群主，进行返现等操作，更新cust_info表等
	
	retcash=1200
	
	updsql="update cust_info set money=money+%d where cust_id= %d"%(retcash,int(old_custid))
	exeUpdate(cur,updsql)


def setgrpmaster(cur,grp_id,cust_id): #设定群主
	setsql="update group_member set group_id = %d ,parent_id=0 where node_id=%d"%(int(grp_id),int(cust_id))
	exeUpdate(cur,setsql)


def flashmem(cur,grp_id,keylist): #刷新群成员信息

	for key in keylist:
		updsql="update group_member set group_id = %d where node_id =%d"%(int(grp_id),int(key))
		exeUpdate(cur,updsql)



#group_member oldgrp_id记录历史插入一份，删除oldgrp群主记录，更新左分支群主组号，更新右分支群主组号,根据左右keylist（custid）逐条遍历，更新组标识
def upgrpmem(cur,oldgrp_id,lgrp_id,rgrp_id,lnewmaster,rnewmaster):
	#插入历史grpmem_his
	hissql="insert grpmem_his select * ,'%s' from group_member where group_id=%d"%(getnowtime(),int(oldgrp_id))
	exeInsert(cur,hissql)

	#删除群主
	delsql="delete from group_member where group_id=%d and parent_id=0 "%(int(oldgrp_id))
	exeDelete(cur,delsql)

	#设定左右群主
	setgrpmaster(cur,lgrp_id,lnewmaster.key)
	setgrpmaster(cur,rgrp_id,rnewmaster.key)


	#获取左右群keylist
	lkeylist=lnewmaster.show_keys()
	rkeylist=rnewmaster.show_keys()
	print("lkeylist",lkeylist)
	print("rkeylist",rkeylist)
	
	#更新左右群组标识
	flashmem(cur,lgrp_id,lkeylist)
	flashmem(cur,rgrp_id,rkeylist)



def divgrp(cur,grp_id):
	
	grouparry=readgrpmem(cur,grp_id) #读取被拆分成员二叉树，返回Binpile类型
	#tierkeylist=grouparry.show_keydelta() #各层级的key列表

	oldmaster,lnewmaster,rnewmaster=grouparry.pop_top() #弹出群主节点，左分支二叉树binpile，右分支二叉树Binpile

	old_custid=oldmaster.key
	lnew_custid=lnewmaster.key
	rnew_custid=rnewmaster.key

	print("old,lnew,rnew==",old_custid,lnew_custid,rnew_custid)

	#更新group_info表，移走老群名称，增加新分裂后的2个新群
	lgrp_id,rgrp_id=credivgrp(cur,old_custid,lnew_custid,rnew_custid) #返回2个新组的组id

	#推出群主，进行返现等操作，更新cust_info表等
	popmaster(cur,old_custid)
	print("pop mater over")

	#group_member oldgrp_id记录历史插入一份，删除oldgrp群主记录，更新左分支群主组号，更新右分支群主组号
	upgrpmem(cur,grp_id,lgrp_id,rgrp_id,lnewmaster,rnewmaster)




if __name__=='__main__':
	grp_id=sys.argv[1]
	
	conn,cur = connDB()
	
	cur.execute("start transaction")
	try:
		divgrp(cur,grp_id)
	except pymysql.err.InternalError as e:
		print("mysql error",e)
		cur.execute("rollback")
	else:
		print("div sucess")
		cur.execute("commit")

	connClose(conn,cur)


