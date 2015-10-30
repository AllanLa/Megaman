
class Queue:
    def __init__( self, capacity=2):
        """ Initialize an empty queue. After finishing this, WHY WOULD ANYONE USE A CIRCULAR ARRAY QUEUE? SO HARD """
        self._array=[None]*capacity
        self._capacity=2
        self._size=0
        self.head=None
        self.head_index=0
        self.tail=None
        self.tail_index=0

        #dequeue and enqueue are O(1), however copying is O(n), if this was a linked list, my Queue would be O(1)
    def isEmpty( self ):
        """ Is the queue empty? 
        Returns True if the queue is empty; False otherwise. """
        if self._size==0:
            return True
        else:
            return False

    def get_size(self):
        return self._size

    def check(self,item):
        """checks the queue to see if an item is in there, returns true if it is else returns false"""
        for x in range(self._size+1):
            if self._array[x]==item:
                return True
        return False

    def enqueue( self, item ):
        """ Push the item onto the back of the queue. """
        if self._array[(self.tail_index+1)%(self._capacity)]!=None:
            self.copy() #if array is full, copies it over to a new array

        if self._size==0:
            self._array[0]=item #if the size is 0, sets the first spot to be the head,tail, indexs are 0
            self.head=item
            self.tail=item
            self.head_index=0
            self.tail_index=0
            self._size+=1
            return

        elif self.tail_index+1==self._capacity:
           #just a specific case to handle the wrapping since the tail is at the end of the array
            self._array[0]=item
            self.tail=item
            self.tail_index=0
            self._size+=1

        else:
            self._array[(self.tail_index+1)%(self._capacity)]=item #sets the next spot to the tail as the item
            self.tail=item #sets the tail as that item
            self.tail_index+=1 #increments tail by 1
            self._size+=1 #increases size by 1

        

    def dequeue( self ):
        """ returns the first item off the queue """
        if self.isEmpty():
            return

        x=self._array[self.head_index] #finds the item to dequeue
        self._array[self.head_index]=None #sets that as none
        self.head=self._array[(self.head_index+1)%self._capacity] #sets the head to be the next one
        self.head_index+=1 #increases head index by 1
        self._size-=1      #decreases size by -1

        return x

    def copy(self):
        """if arrays reaches limit, creates a new one and copys it"""
        new_array=[None]*2*self._capacity
        count=0
        while(self.head_index%self._capacity!=self.tail_index):
            new_array[count]=self._array[self.head_index%self._capacity] #copies everything from head to tail into array
            self.head_index+=1
            count+=1
            
        new_array[count]=self._array[self.tail_index] #the while loop doesnt copy the last one, so this does it
        self._array=new_array #sets the array to be the new one
        self._capacity*=2     #doubles capacity
        self.head=self._array[0] #head is the first one
        self.tail=self._array[count] #tail is the last one
        self.head_index=0 #head is at the first spot
        self.tail_index=count #tail is at the last spot

    def __str__(self):
        """prints the array"""
        x=""
        for i in range(self._capacity):
            x+=str((self._array[i]))+" "

        return x


def main():
    x=Queue()
    x.enqueue(1)
    x.enqueue(2)
    print(x)
    x.dequeue()
    print(x)
    x.enqueue(3)
    print(x)
    x.enqueue(4)
    x.dequeue()
    x.enqueue(5)
    print(x)
    x.dequeue()
    print(x)
    x.enqueue(6)
    x.enqueue(7)
    print(x)
    print("head index is, ",x.head_index)
    print("tail index is, ",x.tail_index)
    x.enqueue(9)
    print(x)