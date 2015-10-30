class Node:
    """A simple Node class

    Data attributes:
        self.data: data of any type to be stored in the node
        self.next: a pointer to the next node. next will be None
            if there are no more nodes.
    """
    def __init__(self, data = None, next = None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev


class Stack:
    """ Implement this Stack ADT using a Python list to hold elements.
         
        Do NOT use the len() feature of lists.
    """

    def __init__( self, capacity=2):
        """ Initialize an empty stack. """
        self.head=None
        self.tail=None
        self.size=0

    def isEmpty( self ):
        """ Is the stack empty? 
        Returns True if the stack is empty; False otherwise. """
        if self.size==0:
            return True
        else:
            return False

    def check(self,item):
        """checks the stack to see if an item is in there, returns true if it is else returns false"""
        if self.head==None:
            return False

        else:
            curr_node=self.head
            while curr_node is not None:
                if curr_node==item:
                    return True
                curr_node=curr_node.next

        return False

    def push( self, item ):
        """ Push the item onto the top of the stack. """
        if self.head==None:
            self.head=Node(item)
            self.tail=self.head
            self.size+=1

        else:
            new_node=Node(item)
            prev_node=self.tail
            self.tail=new_node
            prev_node.next=self.tail
            self.tail.prev=prev_node
            self.size+=1

    def pop( self ):
        """ Pop the top item off the stack and return it. """
        if self.isEmpty():
            return

        if self.size==1:
            x=self.head
            self.head=None
            self.tail=None
            self.size-=1
            return x.data

        else:

            prev_node=self.tail.prev
            data=self.tail.data
            self.tail=prev_node
            prev_node.next=None
            self.size-=1
            return data

    def peek( self ):
        """ Return the top item on the stack (does not change the stack). """
        if self.isEmpty():
            return
        
        return self.tail.data

    def __repr__(self):
        """ Creates a visual representation of the list

        Returns:
            A string of each node's data along with linke arrows
            between them.
        """
        Stack = ""
        curr_node = self.head
        while curr_node is not None:
            Stack += str(curr_node.data) + " -> "
            curr_node = curr_node.next
        return Stack

def main():
    x=Stack()
    x.push(5)
    x.push(2)
    x.push(3)
    print(x)
    x.pop()
    print(x)
    x.pop()
    print(x)
    x.pop()
    print(x.isEmpty())
    x.push(1)
    x.push(3)
    print(x.peek())