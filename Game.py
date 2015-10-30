""" Game to play 'Lost Rovers'. This is the file you edit.
To make more ppm files, open a gif or jpg in xv and save as ppm raw.
Put the three ADTs in their own files.
"""
from gameboard import *
from random import *
from singleLinkedList import*
from stack import*
from Queue import*
import random

class Game:
    SIZE = 15 # rooms are 14x14 (0-14, 0-14)
    def __init__(self):
        # put other instance variables here
        """creates the rover, current room, new room, and a 'count' to keep track of off/on charecteristic """
        self.gui = GameBoard("Megaman Battle Network", self, Game.SIZE)
        self.background="megamanMap.ppm"
        self.rover=Rover(randint(0,14),randint(0,14))
        self.current_room=Room()
        self.home=self.current_room

        self.orientation=1 #facing left will be -1, facing right will be 1, 0 will be no orentiation
        
        self.boss_room=Room()
        self.boss_portal=Portal(self.boss_room, Point(5,0), None, "boss_background.ppm", "boss_portal", "boss_portal.ppm" )
        self.boss_check=False

        self.current_room.set_object(Point(5,0), self.boss_portal)

        self.new_room=None #will be used to create new rooms
        self.on=False      #used so rover will know to step off portal before teleporting again
        self.flashing_portal=None #keeps track of the current flashing portal, after rover steps in, will turn this portal back to normal

        self.inventory=LinkedList() #linked list to hold invetory
        self.tracker=Stack()   #creates a stack that will help Rover find it's way back
        
        self.tasks=Queue()
        self.create_tasks()
        self.current_task=None
        self.step=0           #every 100 steps, will generate another task
        self.last_task=False
        self.task_check=False

        #creates the ship components to the home map

        #adds the ship components to the room at the Point(x,y)
       
        
        self.create_enemys()
        self.add_new_portals_to_current_room() #fills room with 2 portals
        self.add_random_items_to_room() #fills room with random items


    def startGame(self):
        self.gui.run()

    def getRoverImage(self):
        """ Called by GUI when screen updates.
            Returns image name (as a string) of the rover. 
		(Likely 'rover.ppm') """
        return self.rover.get_name()

    def getRoverLocation(self):
        """ Called by GUI when screen updates.
            Returns location (as a Point). """
        # Your code goes here, this code is just an example
        return self.rover.get_position()

    def getImage(self, point):
        """ Called by GUI when screen updates.
            Returns image name (as a string) or None for the 
		part, ship component, or portal at the given 
		coordinates. ('engine.ppm' or 'cake.ppm' or 
		'portal.ppm', etc) """
        
        object=self.current_room.get_object(point)#gets object at that Point
        if object is not None:
            return object.get_image()

        else:
            return None

    def goUp(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        self.step+=1
        position=self.rover.get_position() 
        self.set_portal_check(False) #if two portals are next to each other, this is the back up safety to make sure rover teleports

        if self.orientation==1:
            self.rover.set_name("MegamanRight.ppm")
        else:
            self.rover.set_name("MegamanLeft.ppm")

        if position.y>0:
            self.rover.set_position(0,-1)  #rover cannot go higher than the space, basically acts like the wall

        if self.step==100: #if more than 100 steps are taken, creates another task
            self.create_tasks()
            self.step=0

        position=self.rover.get_position()
        current_object=self.current_room.get_object(position)

        if self.flashing_portal!=None and current_object==self.flashing_portal:
            self.flashing_portal.set_image("portal.ppm")
            self.flashing_portal=None

        if current_object==None:
            self.set_portal_check(False)
            

        else:

            #turns portal check False since the rover stepped off portal
            if current_object.get_name()!="portal":
                self.set_portal_check(False)

            if current_object.get_name()=="boss_portal" and self.boss_check==True:
                map="boss_background.ppm"
                self.gui.set_map(map)
                self.current_room=self.boss_room

            #checks to see if portal has a connection, and if it does not, it creates a new room, and teleports rover to that room
            if type(current_object)==Portal and current_object.get_name()!="boss_portal" and self.get_portal_check()==False and current_object.get_connection()==None:

                self.gui.change_map() #changes the map
                map=self.gui.get_map() #gets the map
                self.background=map #sets the background to be the map
                self.set_portal_check(True) #sets on to be True, so Rover will not teleport until stepping off Portal
                self.create_new_room(self.current_room, position)
                self.add_new_portals_to_current_room() #new room doesn't have portals yet, so adding portals now
                self.add_random_items_to_room() 
                self.create_enemys()

            
            #if the portal already has a connection, then this code takes the rover back to the connected room of that portal
            elif type(current_object)==Portal and self.get_portal_check()==False and current_object.get_connection()!=None:
                prev_portal=current_object.get_connection()  #gets connection of the previous portal
                prev_room=prev_portal.get_data()             #gets the room of that previous portal
                position=prev_portal.get_position()          #gets the position of the previous portal
                self.rover.set_portal_position(position)     #sets the rover position to the previous portal
                self.current_room=prev_room                  #changes the room to the connected room
                self.set_portal_check(True)
                prev_background=prev_portal.get_background() #gets the previous background
                self.background=prev_background 
                self.gui.set_map(self.background) #makes that background the current background


                if self.tracker.peek()==current_object: #if rover goes backwards, pops the portal so it doesn't mess up the way back
                    self.tracker.pop()


                elif not self.tracker.check(prev_portal) and self.current_room!=self.home: #pushes the connected portal onto stack
                    self.tracker.push(prev_portal)



    def goDown(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        self.step+=1
        position=self.rover.get_position()
        self.set_portal_check(False) #if two portals are next to each other, this is the back up safety to make sure rover teleports
        if self.orientation==1:
            self.rover.set_name("MegamanRight.ppm")
        else:
            self.rover.set_name("MegamanLeft.ppm")

        if position.y<14:
            self.rover.set_position(0,1)

        if self.step==100: #if more than 100 steps are taken, creates another task
            self.create_tasks()
            self.step=0

        position=self.rover.get_position()
        current_object=self.current_room.get_object(position)

        if self.flashing_portal!=None and current_object==self.flashing_portal:
            self.flashing_portal.set_image("portal.ppm")
            self.flashing_portal=None

        if current_object==None:
            self.set_portal_check(False)
            

        else:

            #turns portal check False since the rover stepped off portal
            if current_object.get_name()!="portal":
                self.set_portal_check(False)

            if current_object.get_name()=="boss_portal" and self.boss_check==True:
                map="boss_background.ppm"
                self.gui.set_map(map)
                self.current_room=self.boss_room

            #checks to see if portal has a connection, and if it does not, it creates a new room, and teleports rover to that room
            if type(current_object)==Portal and current_object.get_name()!="boss_portal" and self.get_portal_check()==False and current_object.get_connection()==None:
                self.gui.change_map()
                map=self.gui.get_map()
                self.background=map
                self.set_portal_check(True) #sets on to be True, so Rover will not teleport until stepping off Portal
                self.create_new_room(self.current_room, position)
                self.add_new_portals_to_current_room() #new room doesn't have portals yet, so adding portals now
                self.add_random_items_to_room()
                self.create_enemys()

            
            #if the portal already has a connection, then this code takes the rover back to the connected room of that portal
            elif type(current_object)==Portal and self.get_portal_check()==False and current_object.get_connection()!=None:
                prev_portal=current_object.get_connection()  #gets connection of the previous portal
                prev_room=prev_portal.get_data()             #gets the room of that previous portal
                position=prev_portal.get_position()          #gets the position of the previous portal
                self.rover.set_portal_position(position)     #sets the rover position to the previous portal
                self.current_room=prev_room                  #changes the room to the connected room
                self.set_portal_check(True)
                prev_background=prev_portal.get_background()
                self.background=prev_background
                self.gui.set_map(self.background)

                if self.tracker.peek()==current_object: #if rover goes backwards, pops the portal so it doesn't mess up the way back
                    self.tracker.pop()


                elif not self.tracker.check(prev_portal) and self.current_room!=self.home: #pushes the connected portal onto stack
                    self.tracker.push(prev_portal)



    def goLeft(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        self.rover.set_name("MegamanLeft.ppm")
        self.step+=1
        self.orientation=-1
        position=self.rover.get_position()
        self.set_portal_check(False) #if two portals are next to each other, this is the back up safety to make sure rover teleports

        if position.x>0:
            self.rover.set_position(-1,0)
        
        if self.step==100: #if more than 100 steps are taken, creates another task
            self.create_tasks()
            self.step=0

        position=self.rover.get_position()
        current_object=self.current_room.get_object(position)

        if self.flashing_portal!=None and current_object==self.flashing_portal:
            self.flashing_portal.set_image("portal.ppm")
            self.flashing_portal=None

        if current_object==None:
            self.set_portal_check(False)
            

        else:

            #turns portal check False since the rover stepped off portal
            if current_object.get_name()!="portal":
                self.set_portal_check(False)

            if current_object.get_name()=="boss_portal" and self.boss_check==True:
                map="boss_background.ppm"
                self.gui.set_map(map)
                self.current_room=self.boss_room

            #checks to see if portal has a connection, and if it does not, it creates a new room, and teleports rover to that room
            if type(current_object)==Portal and current_object.get_name()!="boss_portal" and self.get_portal_check()==False and current_object.get_connection()==None:
                self.gui.change_map()
                map=self.gui.get_map()
                self.background=map
                self.set_portal_check(True) #sets on to be True, so Rover will not teleport until stepping off Portal
                self.create_new_room(self.current_room, position)
                self.add_new_portals_to_current_room() #new room doesn't have portals yet, so adding portals now
                self.add_random_items_to_room()
                self.create_enemys()

            
            #if the portal already has a connection, then this code takes the rover back to the connected room of that portal
            elif type(current_object)==Portal and self.get_portal_check()==False and current_object.get_connection()!=None:
                prev_portal=current_object.get_connection()  #gets connection of the previous portal
                prev_room=prev_portal.get_data()             #gets the room of that previous portal
                position=prev_portal.get_position()          #gets the position of the previous portal
                self.rover.set_portal_position(position)     #sets the rover position to the previous portal
                self.current_room=prev_room                  #changes the room to the connected room
                self.set_portal_check(True)
                prev_background=prev_portal.get_background()
                self.background=prev_background
                self.gui.set_map(self.background)
                
                if self.tracker.peek()==current_object: #if rover goes backwards, pops the portal so it doesn't mess up the way back
                    self.tracker.pop()


                elif not self.tracker.check(prev_portal) and self.current_room!=self.home: #pushes the connected portal onto stack
                    self.tracker.push(prev_portal)


    def goRight(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        self.rover.set_name("MegamanRight.ppm")
        self.step+=1
        position=self.rover.get_position()
        self.set_portal_check(False) #if two portals are next to each other, this is the back up safety to make sure rover teleports
        self.orientation=1

        if position.x<14:
            self.rover.set_position(1,0)

        if self.step==100: #if more than 100 steps are taken, creates another task
            self.create_tasks()
            self.step=0

        position=self.rover.get_position()
        current_object=self.current_room.get_object(position)

        if self.flashing_portal!=None and current_object==self.flashing_portal:
            self.flashing_portal.set_image("portal.ppm")
            self.flashing_portal=None

        if current_object==None:
            self.set_portal_check(False)
            
        else:

            #turns portal check False since the rover stepped off portal
            if current_object.get_name()!="portal":
                self.set_portal_check(False)

            if current_object.get_name()=="boss_portal" and self.boss_check==True:
                map="boss_background.ppm"
                self.gui.set_map(map)
                self.current_room=self.boss_room

            #checks to see if portal has a connection, and if it does not, it creates a new room, and teleports rover to that room
            if type(current_object)==Portal and current_object.get_name()!="boss_portal" and self.get_portal_check()==False and current_object.get_connection()==None:
                self.gui.change_map()
                map=self.gui.get_map()
                self.background=map
                self.set_portal_check(True) #sets on to be True, so Rover will not teleport until stepping off Portal
                self.create_new_room(self.current_room, position)
                self.add_new_portals_to_current_room() #new room doesn't have portals yet, so adding portals now
                self.add_random_items_to_room()
                self.create_enemys()

            
            #if the portal already has a connection, then this code takes the rover back to the connected room of that portal
            elif type(current_object)==Portal and self.get_portal_check()==False and current_object.get_connection()!=None:
                prev_portal=current_object.get_connection()  #gets connection of the previous portal
                prev_room=prev_portal.get_data()             #gets the room of that previous portal
                position=prev_portal.get_position()          #gets the position of the previous portal
                self.rover.set_portal_position(position)     #sets the rover position to the previous portal
                self.current_room=prev_room                  #changes the room to the connected room
                self.set_portal_check(True)
                prev_background=prev_portal.get_background()
                self.background=prev_background
                self.gui.set_map(self.background)

                if self.tracker.peek()==current_object: #if rover goes backwards, pops the portal so it doesn't mess up the way back
                    self.tracker.pop()


                elif not self.tracker.check(prev_portal) and self.current_room!=self.home: #pushes the connected portal onto stack
                    self.tracker.push(prev_portal)






    def showWayBack(self):
        """ Called by GUI when button clicked.
            Flash the portal leading towards home. """
        if self.tracker.isEmpty() or self.flashing_portal!=None: #if its empty, means you're already home, and if 
            return                                                #portal is not equal to None, cannot click show way back again to mess up stack


        self.flashing_portal=self.tracker.pop() #gets the last portal stacked
        self.tracker.push(self.flashing_portal) #pushes another one onto the stack, so order isn't messed up
        self.flashing_portal.set_image("portal-flashing.ppm") #sets that portal to be flashing
 

    def getInventory(self):
        """ Called by GUI when inventory updates.
            Returns entire inventory (as a string). 
		3 cake
		2 screws
		1 rug
	  """ 

        return str(self.inventory)

    def pickUp(self):
        """ Called by GUI when button clicked. 
		If rover is standing on a part (not a portal 
		or ship component), pick it up and add it
		to the inventory. """
        rover_position=self.rover.get_position()
        current_object=self.current_room.get_object(rover_position)

        if current_object==None or type(current_object)==Portal or type(current_object)==Ship_Component or type(current_object)==Enemy:
            return

        else:
            self.inventory.append(current_object) #adds object to Stack
            self.current_room.set_object(rover_position,None) #sets that as a None

        

    def getCurrentTask(self): #O(1) essentially, #O(n) where n is the length of the current task which is always 3, so O(3)
        """ Called by GUI when task updates.
            Returns top task (as a string). 
        'Fix the engine using 2 cake, 3 rugs' or
        'You win!' 
      """
        if self.current_room==self.boss_room:
            return "HAHAHAHA....\nGame Over!"

        elif self.tasks.isEmpty() and self.last_task: #self.last task is to prevent "you win" after dequeuing last task before finishing #O(1)
            self.boss_check=True
            return "Boss Portal Unlocked, Defeat the Boss!"

        elif self.task_check==True: #O(n) where n is the length of the current task which is always 3, so O(3)
            
            if len(self.current_task)==0:
                self.task_check=False

            x=""
            for i in self.current_task:
                current_object=i.get_data()
                x+=str(i.get_count())+" "+current_object.get_name()+"\n"

            return "Defeat these enimies: \n"+x

        else: #O(n) where n is the length of the current task which is always 3, so O(3)
            self.current_task=self.tasks.dequeue()
            x=""
            for i in self.current_task:
                current_object=i.get_data()
                x+=str(i.get_count())+" "+current_object.get_name()+"\n"

            self.task_check=True
            
            return "Defeat these enimies \n"+x

    def get_orientation(self):
        return self.orientation

    def performTask(self): #will be O(14)*O(n) where n is the size of the invetory
        """ Called by the GUI when button clicked.
            If necessary parts are in inventory, and rover
            is on the relevant broken ship piece, then fixes
            ship piece and removes parts from inventory. If
            we run out of tasks, we win. """

        self.gui.buster_attack() #The worst case scinerio is O(14)
        current_position=self.rover.get_position()#O(1)
        y=current_position.y #O(1)
        orientation=self.orientation #O(1)

        if orientation==1:
            self.rover.set_name("megaman_right_attack.ppm") #sets image to attack right #O(1)
            original_x=current_position.x+1 #gets the original position of megaman #O(1)
            x=current_position.x+1 #gets buster position #O(1)
            while original_x<14: #O(14)*O(n) where n is the length of the task inventory
                for j in self.current_task: #searches each of the task and compares it to the current object
                    current_task_object=j.get_data() #O(1)
                    current_object=self.current_room.get_object(Point(x,y)) #O(1)

                    #basically attacks the enemy, but not part of the Tasks, still erases the enemy but doesnt decrement Task
                    if current_object!=None and current_object.get_name()!=current_task_object.get_name() and type(current_object)==Enemy and self.inventory.get_total_attack()>=200:
                        self.current_room.set_object(Point(x,y), None) #O(1)
                        self.inventory.empty() #empties invetory, 1 attack uses all of the invetory #O(1)
                        return

                    #basically found the enemy in the task suppose to kill, then decrements the amount of that enemy to kill
                    if current_object!=None and current_object.get_name()==current_task_object.get_name() and self.inventory.get_total_attack()>=200:
                        self.current_room.set_object(Point(x,y), None) #O(1)
                        j.increment_count(-1) #O(1)

                        #removes the task if all the enemies are killed
                        if j.get_count()==0: #O(1)
                            self.current_task.remove(j) #O(1)
                        if self.tasks.get_size()==0 and len(self.current_task)==0: #just finished last task, so this back up makes sure "YOU WIN pops up"
                            self.last_task=True #O(1)
                        self.inventory.empty() #O(1)
                        return #O(1) #O(1)
                    x+=1 #O(1)

                x=original_x #O(1)
                original_x+=1 #O(1)

        else:
            self.rover.set_name("megaman_left_attack.ppm") #O(1)
            original_x=current_position.x-1 #O(1)
            x=current_position.x+1 #O(1)
            while original_x>0: #O(14)
                for j in self.current_task: #O(n) where n is the length of the current task
                    current_task_object=j.get_data() #O(1)
                    current_object=self.current_room.get_object(Point(x,y)) #O(1)

                    if current_object!=None and current_object.get_name()!=current_task_object.get_name() and type(current_object)==Enemy and self.inventory.get_total_attack()>=200:#O(1)
                        self.current_room.set_object(Point(x,y), None) #O(1)
                        self.inventory.empty() #O(1)
                        return

                    if current_object!=None and current_object.get_name()==current_task_object.get_name() and self.inventory.get_total_attack()>=200:
                        self.current_room.set_object(Point(x,y), None) #O(1)
                        j.increment_count(-1) #O(1)
                        if j.get_count()==0: #O(1)
                            self.current_task.remove(j) #O(1)

                        if self.tasks.get_size()==0 and len(self.current_task)==0: #just finished last task, so this back up makes sure "YOU WIN pops up"
                            self.last_task=True #O(1)1
                        self.inventory.empty() #O(1)
                        return #O(1)
                    x-=1 #O(1)
                    
                x=original_x #O(1)
                original_x-=1 #O(1)

    def create_enemys(self):
        """creates enemies and adds them to the Room"""
        choices=["Protoman", "Fireman", "Stingman", "Airman"]
        for i in range(3,12):
            for j in range(3,12):
                item=random.choice(choices)
                if self.current_room.get_object(Point(i,j))==None:
                    x=randint(0,25)
                    if x==0:
                        self.current_room.set_object(Point(i,j),Enemy(item,Point(i,j)))

    def create_tasks(self): #O(1) essentially but O(n) if the Queue is full where n is the number of items in the Queue
        """creates tasks for the game"""
        count=0
        task_invetory=[]
        choices=["Protoman", "Fireman", "Stingman", "Airman"]

        while count<3: #O(3)
            x=randint(1,5) #picks a random number between 1-5
            item=random.choice(choices) #picks a random choice
            choices.remove(item) #removes that choice from the list
            task_invetory+=[Task(Enemy(item,None),x)] #adds the the task_invetory the item and number you need
            count+=1

        self.tasks.enqueue(task_invetory)  #stores it into the Queue which is O(1) but if the Queue is full, it will be O(n) where n is amount of items in the Queue before


    def add_new_portals_to_current_room(self):
        """adds two new portals to the current room to random locations"""
        count=0
        while count<2:
            point=Point(randint(3,12),randint(3,12))
            if self.current_room.get_object(point)==None:
                portal=Portal(self.current_room, point, None, self.background, "portal")
                self.current_room.set_object(point,portal)
                count+=1

    def add_random_items_to_room(self):
        """adds random items to the current room in None spots"""
        for i in range(3,12):
            for j in range(3,12):
                if self.current_room.get_object(Point(i,j))==None:
                    x=randint(0,100)
                    if x==0:
                        self.current_room.set_object(Point(i,j), Parts("meteor",False, 40))
                    elif x==1:
                        self.current_room.set_object(Point(i,j), Parts("highcannon",False, 70))
                    elif x==2:
                        self.current_room.set_object(Point(i,j), Parts("longsword",False, 80))
                    elif x==3:
                        self.current_room.set_object(Point(i,j), Parts("varsword", False, 150))

    

    # Put other methods here as needed.
    def create_new_room(self, current_room, point):
        """creates a new room and randomly fills it with parts and connects the current room and the new room to the portals"""
        
        current_portal=current_room.get_object(point) #gets the current portal


        self.new_room=Room()  #creates the new room
        for i in range(3,12):   #randomly adds objects to the new room
            for j in range(3,12):
                x=randint(0,100)
                if x==0:
                    self.current_room.set_object(Point(i,j), Parts("meteor",False, 40))
                elif x==1:
                    self.current_room.set_object(Point(i,j), Parts("highcannon",False, 70))
                elif x==2:
                    self.current_room.set_object(Point(i,j), Parts("longsword",False, 80))
                elif x==3:
                    self.current_room.set_object(Point(i,j), Parts("varsword", False, 150))
                else:
                    self.new_room.set_object(Point(i,j), None)

        new_portal=Portal(self.new_room, None, None, self.background)   #creates a new portal with the new room as the data attribute

        while True:
            position=Point(randint(0,14), randint(0,14))
            if self.new_room.get_object(position)==None:   #finds a position to set the new portal object
                break

        self.new_room.set_object(position, new_portal) #sets the portal at the location
        new_portal.set_position(position)          #gives the portal a location charecteristic
        self.rover.set_portal_position(position)   #puts the rover on top of the new portal
        current_portal.set_connection(new_portal)  #connects the two portals
        new_portal.set_connection(current_portal)
        self.current_room=self.new_room             #changes the current room to the new room
        self.tracker.push(new_portal)               #pushes the new portal onto the stack
    
    def get_portal_check(self):
        """returns portal check"""
        return self.on

    def set_portal_check(self,statement):
        """makes sure rover has to get off portal before teleporting"""
        self.on=statement


# Put other classes here or in other files as needed.
class Task:
    """ A task class that will hold how much of something one needs"""
    def __init__(self, data, count=0):
        self.data=data
        self.count=count

    def get_data(self):
        return self.data

    def get_count(self):
        return self.count

    def increment_count(self, value):
        self.count+=value


class Enemy():
    def __init__(self, name, position=None):
        self.name=name
        self.position=position

    def get_image(self):
        return self.name+".ppm"

    def get_position(self):
        return self.position

    def get_name(self):
        return self.name




class Rover:
    def __init__(self, x, y):
        """creates a rover object with a position and name"""
        self.rover="MegamanRight.ppm"
        self.position=Point(x,y)

    def get_position(self):
        """returns the position of the rover"""
        return self.position

    def set_position(self,horizontalShift,verticalShift):
        """Sets the position of the rover by the shifts"""
        position = self.get_position()
        x = position.x
        y = position.y
        
        self.position=Point(x+horizontalShift,y+verticalShift)

    def set_portal_position(self,position):
        """Sets Rover on top of portal"""
        x=position.x
        y=position.y

        self.position=Point(x,y)

    def set_name(self,name):
        self.rover=name

    def get_name(self):
        return self.rover

class Room:
    def __init__(self):
        """creates a 2D list to represent the Room"""
        self.room=[]
        for i in range(15):
            self.room+=[[None]*15]

    def set_object(self,Point,Object):
        """sets an object at the specific Point in the Current Room"""
        self.room[Point.x][Point.y]=Object

    def get_object(self,Point):
        """returns the object at that point"""
        return self.room[Point.x][Point.y]


    def __repr__(self):
        """used for debugging, prints the current room"""

        x=""
        for i in range(15):
            for j in range(15):
                if self.room[j][i]!=None:
                    x+=self.room[j][i].get_name()+" "
                else:
                    x+="None "

            x+="\n"

        return x



class Ship_Component:
    def __init__(self,name,broken,count=0):
        """creates an object of that type Ship Component, and this object is broken or not"""
        self.name=name
        self.broken=broken
        self.count=count

    def get_name(self):
        """returns name of the object"""
        return self.name

    def is_broken(self):
        """returns true/false if its broken or not"""
        return self.broken

    def get_image(self):
        """returns the image of the object"""
        if self.is_broken():
            return self.get_name()+"broken.ppm"

        else:
            return self.get_name()+".ppm"

    def get_count(self):
        return self.count

    def fixed(self):
        self.broken=False

class Parts(Ship_Component):
    def __init__(self,name,broken,attack_points=0):
        self.broken=broken
        self.name=name
        self.attack_points=attack_points

    def get_attack(self):
        return self.attack_points

class Portal:
    """Portal is basically a node, the self.data would be the current
       room, and connection represents next and before"""
    
    def __init__(self, data=None, position=None, connection=None, background=None, name="portal", image="portal.ppm"):
        """creates a portal object with a data,position,connection, and name attributes"""
        self.data=data
        self.connection=connection
        self.image=image
        self.name=name
        self.position=position
        self.portal_background=background

    def get_name(self):
        """returns the name"""
        return self.name

    def set_image(self,name):
        self.image=name

    def get_data(self):
        """returns the data of the portal"""
        return self.data

    def get_background(self):
        return self.portal_background

    def get_connection(self):
        """returns the connection of the portal"""
        return self.connection

    def set_connection(self,connection):
        """sets connection for the portal"""
        self.connection=connection

    def get_position(self):
        """returns the position of the portal"""
        return self.position

    def set_position(self,point):
        """sets the position of the portal"""
        self.position = point

    def get_image(self):
        """returns the image name"""
        return self.image


""" Launch the game. """
g = Game()
g.startGame() # This does not return until the game is over
