from sys import getsizeof

class Node:
	"""A simple Node class

	Data attributes:
		self.data: data of any type to be stored in the node
		self.next: a pointer to the next node. next will be None
			if there are no more nodes.
	"""
	def __init__(self, data = None, next = None,count=1):
		self.data = data
		self.next = next
		self.count=1

	def increment_node(self,value):
		"""increments the count by value"""
		self.count+=value

	def quantity(self):
		"""returns the count of how many items there are"""
		return self.count

	def increment_quantity(self,value):
		self.count+=value

	def get_name(self):
		return self.data.get_name()

class LinkedList:
	"""A basic Linked List data structure

	Data attributes:
	 self.head: a reference to the first Node in the list.
		self.head will be None if the list is empty
	"""

	def __init__(self, python_list = None):
		""" Initializes a new linked list.

		If no arguments are provided, an empty list is created.
		Otherwise, a python
		"""
		self.head = None
		if python_list is not None:
			self._create_list(python_list)

		self.total=0

	def empty(self):
		self.head=None
		
	def __str__(self):
		""" Creates a visual representation of the list

		Returns:
			A string of each node's data along with linke arrows
			between them.
		"""
		self.check()
		linked_list = ""
		curr_node = self.head
		count=0
		while curr_node:
			count+=curr_node.data.get_attack()*curr_node.quantity()
			if curr_node.quantity()>0:
				linked_list += str(curr_node.quantity()) + " "+curr_node.data.get_name()+" | "+str(curr_node.data.get_attack())+" ATK"
				linked_list+="\n"
				curr_node = curr_node.next

		linked_list+="TOT ATK | "+str(count)
		self.attack=count
		return linked_list

	def get_total_attack(self):
		return self.attack

	def get_size_of(self):
		curr_size = 0

		curr_node = self.head
		while curr_node is not None:
			curr_size += getsizeof(curr_node)
			curr_node = curr_node.next

		return curr_size


	# ----------- BASIC OPERATIONS --------------#
	def append(self, data):
		""" Appends a new node containing data at the end of the list.

		Args:
			data: the data that will be appended to the current list
		"""
		new_node = Node(data, None, 1)
		if self.head is None:
			self.head = new_node
		else: 
			curr_node = self.head
			while curr_node.next is not None: 
				if curr_node.data.get_name()==new_node.data.get_name(): #searches until it finds the same type
					curr_node.increment_node(1) #if it finds the same time, increment that count by 1
					return  #break after
				curr_node = curr_node.next

			if curr_node.data.get_name()==new_node.data.get_name(): #backup safety incase last one is same type
				curr_node.increment_node(1)
				return

			curr_node.next = new_node  #if it goes all the way and doesnt find the item, sets the new node as next


	def check(self):
		"""checks to see if items have count above 0, if not, remove them from the list"""
		if self.get_size_of()==0:
			self.head=None
			return

		curr_node=self.head
		prev_node=self.head

		if curr_node.quantity()<1 and curr_node==self.head: #first checks the head, and if head is 0
				next_node=self.head.next                        #then sets the head to be the next
				self.head=next_node
				curr_node=self.head

		while curr_node is not None:
			if curr_node.quantity()<1:                        
				prev_node.next=curr_node.next       #sets previous node next to current node's next 
				curr_node=curr_node.next            #thus deleting the element with 0 quantity

			else:
				prev_node=curr_node
				curr_node=curr_node.next




	def pop(self):
		""" Removes (and returns the data at) the last node of the list.

		If the list is empty, throw an error

		Returns:
			The data at the last element in the list
		"""
		assert self.head is not None, "Cannot pop an empty list"
		prev_node = None
		curr_node = self.head

		while curr_node.next:
			prev_node = curr_node
			curr_node = curr_node.next

		if prev_node is not None:
			prev_node.next = None
		return curr_node.data

