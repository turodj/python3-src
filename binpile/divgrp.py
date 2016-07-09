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

	pass
	#return(lgrp_id,rgrp_id)

#group_member oldgrp_id记录历史插入一份，删除oldgrp群主记录，更新左分支群主组号，更新右分支群主组号,根据左右keylist（custid）逐条遍历，更新组标识
def upgrpmem(cur,oldgrp_id,lgrp_id,rgrp_id,lnewmaster,rnewmaster):
	pass

def divgrp(cur,grp_id):
	
	grouparry=readgrpmem(cur,grp_id) #读取被拆分成员二叉树，返回Binpile类型
	#tierkeylist=grouparry.show_keydelta() #各层级的key列表

	oldmaster,lnewmaster,rnewmaster=grouparry.pop_top() #弹出群主节点，左分支二叉树binpile，右分支二叉树Binpile

	old_custid=oldmaster.key
	lnew_custid=lnewmaster.key
	rnew_custid=rnewmaster.key

	#更新group_info表，移走老群名称，增加新分裂后的2个新群
	lgrp_id,rgrp_id=credivgrp(cur,old_custid,lnew_custid,rnew_custid) #返回2个新组的组id

	#group_member oldgrp_id记录历史插入一份，删除oldgrp群主记录，更新左分支群主组号，更新右分支群主组号
	upgrpmem(cur,grp_id,lgrp_id,rgrp_id,lnewmaster,rnewmaster)



	#qrysql="select * from group_member where group_id = %d order by seq"%(int(grp_id))

	#exeSelect(cur,qrysql)

	#memdata=list(cur.fetchall())

	#groupinfo=memdata.pop(0) #第一行是组信息，建立组
	##seq,g,node,parent,left_flag,right_flag=groupinfo
	#masternode=str(groupinfo[2])

	#grouparry=Binpile(masternode) #根据群主建群

	#nodelist=[]
	#for record in memdata:
	#	
	#	seq,g,node,parent,left_flag,right_flag=record
	#	#print(node,type(node))
	#	nodelist.append(str(node))
	#
	#

	#grouparry.bappend(nodelist)

	##tmplist=grouparry.show_delta()
	##
	##for t in tmplist:
	##	print(t)
	#return(grouparry)



if __name__=='__main__':
	grp_id=sys.argv[1]
	
	conn,cur = connDB()
	
	cur.execute("start transaction")
		if divgrp(cur,grp_id) != False:
			cur.execute("commit")
		else:
			cur.execute("rollback")
		

	#tmplist=grouparry.show_delta()
	
	#for t in tmplist:
	#	print(t)

	connClose(conn,cur)


