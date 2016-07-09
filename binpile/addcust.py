# -*- coding: UTF-8 -*



import socket,sys,os
import re
import urllib
import sys,time
import pymysql

from binpile import Binpile

def connDB():
	conn=pymysql.connect("127.0.0.1",unix_socket="/tmp/mysql.sock",user="root",passwd="turodj",db="mysql",charset="utf8")
	cur=conn.cursor()
	cur.execute("use binpile")
	return(conn,cur)


def exeSelect(cur,sql):
	cur.execute("commit") #刷新cur
	cur.execute(sql)
	return(cur)

def exeInsert(cur,sql):#更新语句，可执行insert,delete语句
    sta=cur.execute(sql);
    return(sta);

def exeDelete(cur,sql):#更新语句，可执行delete语句
    sta=cur.execute(sql);
    return(sta);

def exeUpdate(cur,sql):#更新语句，可执行update语句
    sta=cur.execute(sql);
    return(sta);

def connClose(conn,cur):#关闭所有连接
    cur.close();
    conn.close();

def addcust(cust_name,phone_no,money): #cust_id 自增，不用显性插入
	conn,cur = connDB()
	addsql="insert cust_info(cust_name,phone_no,money) values('%s','%s',%d)"%(cust_name,phone_no,int(money)) #输入汉字还是不行，cust_name汉字编码问题需要解决

	print(addsql)

	stat=exeInsert(cur,addsql)
	if stat == 1:
		print("sucess")
		cur.execute("commit")
	else:
		print("fail")
		cur.execute("rollback")



	connClose(conn,cur)

if __name__ == "__main__":
	cust_name=sys.argv[1]
	phone_no=sys.argv[2]
	money=sys.argv[3]
	print(cust_name,phone_no,money,type(money))
	addcust(cust_name,phone_no,money)

	
