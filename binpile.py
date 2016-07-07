
import socket,sys,os
import re
import urllib
import sys,time

class Binpile(object):
	"""docstring for Binpile"""
	#__slots__=("key","left_node","right_node")

	def __init__(self,root):
		self.key=root
		self.left_node=None
		self.right_node=None
		self.parent=None
	
	def __str__(self):
		return self.key
	
	__repr__ = __str__

	def set_key(self,name):
		if self.key==None:
			self.key=name
			return True
		else:
			return False
	
	def isroot(self): #判断是否根节点
		if self.parent==None:
			return True
		else:
			return False
	
	def ins_left(self,newnode):#为空插入左节点
		if self.left_node==None:
			self.left_node=Binpile(newnode)
			self.left_node.parent=self
			return self.left_node
		else:
			return False
	
	def ins_right(self,newnode):#为空插入右节点
		if self.right_node==None:
			self.right_node=Binpile(newnode)
			self.right_node.parent=self
			return self.right_node
		else:
			return False	
	
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

	#根据将序列依次插入二叉堆
	def bappend(self,nodelist):
		if isinstance(nodelist,list)==False: #判断入参是否是序列
			return("input nodelist not list\n")
		if self==None:#判断根节点是空，返回
			return("root is none")

		listres=nodelist.copy()
		stack=[self] #根节点放入列表		

		while stack:
			if len(listres) == 0: #节点添加完，跳出循环
				break

			current=stack.pop(0)
			if current.left_node==None: #左节点为空，获取资料list第一个节点，插入做节点，然后把左节点压入循环序列
				insnode=listres.pop(0)
				current.ins_left(insnode)
				stack.append(current.left_node)
			else:
				stack.append(current.left_node) #不为空，下滑一位

			if len(listres) == 0: #节点添加完，跳出循环
				break
			if current.right_node==None:
				insnode=listres.pop(0)
				current.ins_right(insnode)
				stack.append(current.right_node)
			else:
				stack.append(current.right_node)
		return self


	#展示二叉堆所有节点，水平层级展示
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



	#利用列表形成堆栈机制，进行二叉树侧水平层次遍历,形成迭代器
	def get_iter(self):
		stack=[self] #根节点放入列表
		while stack:
			current=stack.pop(0)
			yield current
			if current.left_node:
				stack.append(current.left_node)
			if current.right_node:
				stack.append(current.right_node)


			
