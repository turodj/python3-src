
# -*- coding: UTF-8 -*
#定义了二叉堆的类和方法


import socket,sys,os
import re
import urllib
import sys,time


class Binpile(object):
	"""docstring for Binpile"""
	#二叉堆对象，key是唯一标识
	#__slots__=("key","left_node","right_node")

	def __init__(self,root):
		self.key=root
		self.master=False
		self.value=None
		self.left_node=None
		self.right_node=None
		self.parent=None
	
	def __str__(self):
		return self.key
	
	__repr__ = __str__

	#定义根据key取值,返回Binpile节点对象
	def __getitem__(self,key):
		stack=[self] #根节点放入列表
		while stack:
			current=stack.pop(0)
			#print(current)
			
			if current.key==key:
				return current

			if current.left_node:
				stack.append(current.left_node)
			if current.right_node:
				stack.append(current.right_node)
		else:
			return False


	def set_key(self,name):
		if self.key==None:
			self.key=name
			return True
		else:
			return False
	
	def isroot(self): #判断是否根节点
		if self.parent is None:
			return True
		else:
			return False
	
	def ins_left(self,newnode):#为空插入左节点
		if self.get_key(newnode) != False: #判断此key是否已在二叉树中
			return False
		if self.left_node==None:
			self.left_node=Binpile(newnode)
			self.left_node.parent=self
			return self.left_node
		else:
			return False
	
	def ins_right(self,newnode):#为空插入右节点,并且左节点不为空，构建完全二叉树
		
		if self.get_key(newnode) != False: #判断此key是否已在二叉树中
			return False

		if self.right_node==None and self.left_node!=None:
			self.right_node=Binpile(newnode)
			self.right_node.parent=self
			return self.right_node
		else:
			return False	
	
	def get_high(self):  
	   node_temp=self
	   high=0
	   lth=0

	   if node_temp != None:
	   	high+=1

	   	#递归获取子节点层级长度
	   	if node_temp.left_node!=None:
	   		tmp_left=node_temp.left_node
	   		lth = tmp_left.get_high()
	   		high += lth

	   return high

	#获取二叉堆的层级和节点数
	def get_size(self):
		node_temp=self
		high=0
		lenth=0
		lth=0
		ltl=0
		rth=0
		rtl=0

		if node_temp!=None:
			high+=1
			lenth+=1
			#递归获取子节点层级长度
			if node_temp.left_node!=None:
				tmp_left=node_temp.left_node
				lth,ltl = tmp_left.get_size()
				high += lth
				lenth += ltl
			#递归获取右子节点长度
			if node_temp.right_node!=None:
				tmp_right=node_temp.right_node
				rth,rtl = tmp_right.get_size()
				lenth += rtl

		return high,lenth
	
	
	#获取所有keys
	def show_keys(self):
		stack=[self] #根节点放入列表
		keylist=[] #用于返回的序列
		while stack:
			current=stack.pop(0)
			#print(current)
			keylist.append(current.key) #把获取的节点增加进然后序列

			if current.left_node:
				stack.append(current.left_node)
			if current.right_node:
				stack.append(current.right_node)
		return keylist
	

	#根据将序列依次插入二叉堆
	def bappend(self,keylist):
		if isinstance(keylist,list)==False: #判断入参是否是序列
			return("input nodelist not list\n")
		if self==None:#判断根节点是空，返回
			return("root is none")
		
		#判断是否存在重复的key
		allkeys=self.show_keys()
		coverkey=set(allkeys)&set(keylist) 

		if len(coverkey)!= 0:
			return("already contain ",coverkey)

		#依次插入到二叉堆中
		listres=keylist.copy()
		stack=[self] #根节点放入列表		

		while stack:
			if len(listres) == 0: #节点添加完，跳出循环
				break

			current=stack.pop(0)
			if current.left_node==None: #左节点为空，获取资料list第一个节点，插入做节点，然后把左节点压入循环序列
				insnode=listres.pop(0)
				if current.ins_left(insnode) != False:
					stack.append(current.left_node)
				else:
					break
			else:
				stack.append(current.left_node) #不为空，下滑一位

			if len(listres) == 0: #节点添加完，跳出循环
				break
			if current.right_node==None:
				insnode=listres.pop(0)
				if current.ins_right(insnode) != False:
					stack.append(current.right_node)
				else:
					break
			else:
				stack.append(current.right_node)
		return self


	#展示二叉堆所有节点，水平层级展示,返回所有节点列表
	def show_all(self):
		stack=[self] #根节点放入列表
		nodelist=[] #用于返回的序列
		while stack:
			current=stack.pop(0)
			#print(current)
			nodelist.append(current) #把获取的节点增加进然后序列

			if current.left_node:
				stack.append(current.left_node)
			if current.right_node:
				stack.append(current.right_node)
		return nodelist
	
	#以树形结构展示二叉堆，返回二级链表
	def show_delta(self):
		nodelist=self.show_all()
		treehigh=self.get_high()
		tier=[]
		templist=[]
		for i in range(0,treehigh):
			templist=nodelist[pow(2,i)-1:pow(2,i+1)-1]
			tier.append(templist)
		return tier


	

	#根据key值获取节点
	def get_key(self,key):
		stack=[self] #根节点放入列表
		while stack:
			current=stack.pop(0)
			#print(current)
			
			if current.key==key:
				return current

			if current.left_node:
				stack.append(current.left_node)
			if current.right_node:
				stack.append(current.right_node)
		else:
			return False
	
	#根据key值获取其祖先, 回溯返回其祖先序列
	def get_grand(self,key):
		grandlist=[]
		keynode=self.get_key(key)
		if keynode!=False:
			parentnode=keynode.parent
			while parentnode:
				grandlist.append(parentnode)
				parentnode=parentnode.parent
		return grandlist
	
	#弹出顶端节点，返回，top节点，以及其后分成的两个节点
	def pop_top(self):
		if self.isroot==False:
			return("It not root")
		
		leftnewmaster=self.left_node
		self.left_node=None
		
		rightnewmaster=self.right_node
		self.right_node=None

		topnode=self
		return topnode,leftnewmaster,rightnewmaster






			
