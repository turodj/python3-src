# -*- coding: UTF-8 -*
#批量随机生成号码、名称；执行方法 python3 patchaddcust.py 


import socket,sys,os
import re
import urllib
import sys,time
import pymysql
import random

from binpile import Binpile
from binmysql import * #可以应用binmysql.py中的函数
from addcust  import *




if __name__ == "__main__":
	
	fnamebin=["董","耿","吴","黄","党","李","顾","仲"]
	secnamebin=[" ","水","建","继","春","小","旭","妮"]
	trinamebin=["健","颖","华","玲","利","颜","严","红"]


	
	for  i in range(50):
		cust_name=random.choice(fnamebin)+random.choice(secnamebin)+random.choice(trinamebin)
		phone_no=random.randint(18600000000,18609999999)
		print(cust_name,phone_no)
		addcust(cust_name,phone_no,600)
	
	

	
