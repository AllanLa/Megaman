""" A square gameboard that draws colored tiles. Includes text fields for
a task and inventory. Includes buttons to play the game.

Uses the graphics class that John Zelle wrote to use with
"Python Programming: An Introduction to Computer Science" (Franklin,
Beedle & Associates). Uses the GraphWin, Rectangle, and Text classes. Adds
in a Button class.

Students do not have to edit this file.

-----------------------------------------------------------------------
COPYRIGHT: Lea Wittie 2014

LICENSE: This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    This is open-source software released under the terms of the
    GPL (http://www.gnu.org/licenses/gpl.html). 

PLATFORMS: The package requires Tkinter and should run on
any platform where Tkinter is available.

INSTALLATION: Put this file somewhere where Python can see it. Also get a
copy of graphics.py as mentioned above.

CREDITS: Original file by Lea Wittie. Bug in quit function fixed by Matt Rogge '17
"""
from graphics import *
from functools import partial
import tkinter as tk
import random

class GameBoard:
    """ A game board of size X size squares with fields for tasks and inventory,
        and many buttons. """

        # Otherwise, type the key on the screen
    # draw the board

    def __init__(self, title, game, size, bkColor='maroon', buttonColor='LightSalmon'):
        """ Takes a title to display on top of the window.
            Takes a game which implements the following methods:
                goLeft(), goRight(), goUp(), goDown(), showWayBack(), pickUp(), performTask()
            Color options: http://packages.python.org/ete2/reference/reference_svgcolors.html    
        """
        width = 650
        height = 600
        self.size = size

        self.game = game 
        self.window = GraphWin(title, width, height)
        self.window.setBackground(bkColor)
        self.background="megamanMap.ppm"

        sideOffset = 10  # offset from sides
        lineSpace = 25   # vertical offset between lines
        boxOffset = 5    # offset from side of box
        taskHeight = 100 # height of task window where tasks are listed
        taskWidth = 400
        self.mapSize = (400//self.size)*self.size  # height of map window where map is seen
        invHeight = 300 # height of inv window where inventory is listed
        invWidth = 200
        buttonWidth = 200 # width of the button space
        
        # top left is Task Window
        taskX = sideOffset
        taskY = sideOffset
        taskLabel = Text(Point(taskX, taskY), "Task")
        taskLabel.setStyle('bold')
        taskLabel.draw(self.window)
        taskRect = Rectangle(Point(taskX, taskY + lineSpace), Point(taskX + taskWidth, taskY + lineSpace + taskHeight))
        taskRect.setFill("white")
        taskRect.draw(self.window)
        self.taskWin = Text(Point(taskX + boxOffset, taskY + lineSpace + boxOffset), " ")
        self.taskWin.draw(self.window)

        # bottom left is Room Map
        mapX = sideOffset
        mapY = sideOffset + lineSpace + taskHeight + lineSpace
        self.mapRectX = mapX
        self.mapRectY = mapY + lineSpace
        mapLabel = Text(Point(mapX, mapY), "Map of room")
        mapLabel.setStyle('bold')
        mapLabel.draw(self.window)
        self.mapRect = Rectangle(Point(mapX, mapY + lineSpace),
                            Point(mapX + self.mapSize,
                                  mapY + lineSpace + self.mapSize))
        self.mapRect.setFill("white")
        self.mapRect.draw(self.window)

        # top right is Inventory
        invX = width - sideOffset - invWidth
        invY = sideOffset
        invLabel = Text(Point(invX, invY), "Inventory")
        invLabel.setStyle('bold')
        invLabel.draw(self.window)
        invRect = Rectangle(Point(invX, invY + lineSpace), Point(invX + invWidth, invY + lineSpace + invHeight))
        invRect.setFill("white")
        invRect.draw(self.window)
        self.invWin = Text(Point(invX + boxOffset, invY + lineSpace + boxOffset), " ")
        self.invWin.draw(self.window)

        # bottom right is buttons
        buttonX = sideOffset + self.mapSize + lineSpace
        buttonY = sideOffset + lineSpace + invHeight + lineSpace
        self.up = Button(Point(buttonX + buttonWidth/2, buttonY),
                         "^", partial(self.do, self.game.goUp), buttonColor)
        self.up.draw(self.window)
        self.down = Button(Point(buttonX + buttonWidth/2, buttonY + lineSpace*2),
                           "V", partial(self.do, self.game.goDown), buttonColor)
        self.down.draw(self.window)
        self.left = Button(Point(buttonX + buttonWidth*3/8, buttonY + lineSpace),
                           "<--", partial(self.do, self.game.goLeft), buttonColor)
        self.left.draw(self.window)
        self.right = Button(Point(buttonX + buttonWidth*5/8, buttonY + lineSpace),
                            "-->", partial(self.do, self.game.goRight), buttonColor)
        self.right.draw(self.window)
        self.wayBack = Button(Point(buttonX + buttonWidth/2, buttonY + lineSpace*4),
                              "Show the way back",
                              partial(self.do, self.game.showWayBack), buttonColor)
        self.wayBack.draw(self.window)
        self.pickUp = Button(Point(buttonX + buttonWidth*1/4, buttonY + lineSpace*6),
                             "Pick up",
                             partial(self.do, self.game.pickUp), buttonColor)
        self.pickUp.draw(self.window)
        self.performTask = Button(Point(buttonX + buttonWidth*3/4, buttonY + lineSpace*6),
                                  "Attack",
                                  partial(self.do, self.game.performTask), buttonColor)
        self.performTask.draw(self.window)
        self.quit = Button(Point(buttonX + buttonWidth*1/4, buttonY + lineSpace*8),
                           "Quit", self.quit, buttonColor)
        self.quit.draw(self.window)
        self.help = Button(Point(buttonX + buttonWidth*3/4, buttonY + lineSpace*8),
                           "Help", self.nothing, buttonColor)
        self.help.draw(self.window)

        self.images = []
        for x in range(self.size):
            self.images.append([])
            for y in range(self.size):
                self.images[x].append(None)

        self.isUpdating = False # to handle overlapping calls to updateGUI()

    def do(self, fncn):
        """ Wrapper class that runs the provided function and then
            updates the GUI. """
        if self.isUpdating:
            return
        fncn()
        self.updateGUI()

    def change_map(self):
        x=random.choice(["megamanMap.ppm","megamanMap2.ppm", "megamanMap3.ppm"])
        self.set_map(x)

    def set_map(self, map):
        self.background=map

    def get_map(self):
        return self.background

    def updateGUI(self):
        """ Update the GUI (tasks, inventory, grid) """
        self.isUpdating = True
        #updates the background
        tileLength = self.mapSize//self.size
        loc = Point(7,7)
        i = Image(Point(self.mapRectX + loc.x*tileLength + tileLength//2,
                                 self.mapRectY + loc.y*tileLength + tileLength//2),
                           tileLength,tileLength)
        i.setImage(self.background)
        i.draw(self.window)


        # Update the stuff on the grid (items, portals, ship components)
        for x in range(self.size):
            for y in range(self.size):
                image = self.game.getImage(Point(x,y))
                               
                # if image was in location and has changed or gone, erase it
                if self.images[x][y] != None and self.images[x][y].getImage()!=image:
                    self.images[x][y].undraw()
                
                # if image is now there and wasn't before
                if image != None and self.images[x][y] == None:
                    i = Image(Point(self.mapRectX + x*tileLength + tileLength//2,
                                     self.mapRectY + y*tileLength + tileLength//2),
                            tileLength,tileLength)
                    i.setImage(image)
                    i.draw(self.window)
                    self.images[x][y] = i

                # if image was there and has changed
                elif image != None and self.images[x][y] != None and self.images[x][y].getImage()!=image:
                    self.images[x][y].setImage(image)
                    self.images[x][y].draw(self.window)
                
                # if now gone
                elif image == None and self.images[x][y] != None:
                    self.images[x][y] = None

                elif self.images[x][y] != None and self.images[x][y].getImage()==image:
                    self.images[x][y].setImage(image)
                    self.images[x][y].undraw()
                    self.images[x][y].draw(self.window)

                # error checking.. nothing should print
                elif image == None and self.images[x][y] == None:
                    pass
                elif self.images[x][y] != None and image == self.images[x][y].getImage():
                    pass
                else:
                    string = '['+str(x)+']['+str(y)+'] image:' + str(image) + ', stored image:'
                    if self.images[x][y] == None:
                        string += 'None'
                    else:
                        string += self.images[x][y].getImage()
                    print(string)
                
        # Update the rover
        rover = self.game.getRoverImage()
        loc = self.game.getRoverLocation()
        try: # decently non-flickery
            self.rover.undraw()
        except Exception:
            pass
        if loc != None and rover != None:
            self.rover = Image(Point(self.mapRectX + loc.x*tileLength + tileLength//2,
                                     self.mapRectY + loc.y*tileLength + tileLength//2),
                               tileLength,tileLength)
            self.rover.setImage(rover)
            self.rover.draw(self.window)

        # Update the task field
        taskText = self.game.getCurrentTask()
        oldTaskText = self.taskWin.config["text"]
        if taskText != None and taskText != oldTaskText:
            self.taskWin.undraw()
            self.taskWin.config["text"] = taskText
            self.taskWin.draw(self.window)

        # Update the inventory field
        invText = self.game.getInventory()
        oldInvText = self.invWin.config["text"]
        if invText != None and invText != oldInvText:
            self.invWin.undraw()
            self.invWin.config["text"] = invText
            self.invWin.draw(self.window)

        self.isUpdating = False

    def buster_attack(self): #worse case scinerio is O(14)
        """updates the drawing a "shot" in x location, then deleting it and putting it to the roll over"""
        tileLength = self.mapSize//self.size
        orientation=self.game.get_orientation() #gets Megamans direction, whether he is facing left or right
        if orientation==1:
            shot_orientation="megaman_right_buster_attack.ppm"
        else:
            shot_orientation="megaman_left_buster_attack.ppm"

        current_position=self.game.getRoverLocation() #O(1) #gets location of megaman
        x=current_position.x
        y=current_position.y
        shot=Buster(Point(x+orientation,y), shot_orientation)  #sets location of that shot to be left or right of megaman
        x=shot.get_name()
        loc =shot.get_position()

        if orientation==1:
            while loc.x<=14: #basically updates the shot going across to the right
                i = Image(Point(self.mapRectX + loc.x*tileLength + tileLength//2,
                                     self.mapRectY + loc.y*tileLength + tileLength//2),
                               tileLength,tileLength)
                i.setImage(x)
                i.draw(self.window)
                shot.increment_right()
                loc=shot.get_position()
        else:
            while loc.x>=0: #basically updates the shot going across to the left
                i = Image(Point(self.mapRectX + loc.x*tileLength + tileLength//2,
                                     self.mapRectY + loc.y*tileLength + tileLength//2),
                               tileLength,tileLength)
                i.setImage(x)
                i.draw(self.window)
                shot.increment_left()
                loc=shot.get_position()


        
    def nothing(self):
        """ Called by the help button. Could be replaced by a function
            that actually does something. """
        print('Rules:\n1.Attacking uses all of the Attack Points\n2.Pick up Weapons to increase Attack Points\n3. Each enemey has 200 life points.\n4.Just kill enimies')

    def run(self):
        """ Repeatedly wait for a click.. Keeps the game running. """
        self.updateGUI()
        self.shouldRun = True
        
        while(self.shouldRun):
            try:
                pt = self.window.getMouse()
            except Exception:
                pass


    def quit(self):
        """ Called by the quit button. Closes the window and forces the run
            loop to terminate.
        """
        self.window.close()
        self.shouldRun = False

class Buster:
    """Buster Class to represent Megaman's Attack"""
    def __init__(self,position, name):
        self.position=position
        self.name=name

    def increment_right(self):
        x=self.position.x+1
        y=self.position.y
        self.position=Point(x,y)

    def increment_left(self):
        x=self.position.x-1
        y=self.position.y
        self.position=Point(x,y)

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position