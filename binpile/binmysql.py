# -*- coding: UTF-8 -*
#定义数据库相关函数


import socket,sys,os
import re
import urllib
import sys,time
import pymysql





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

def getnowtime():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    nowtime=time.strftime( ISOTIMEFORMAT, time.localtime())
    return(nowtime)
