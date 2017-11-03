#!/usr/bin/env python3
# ##################################################################
#
# CSSE1001/7030 - Assignment 3
#
#   Student Username: s4382911
#
#   Student Name: Arda Akgur
#
#   Version: 1.0.0
#
###################################################################

###################################################################
#
# The following is support code. DO NOT CHANGE.

from assign3_support import *


# End of support code
################################################################
# Write your code below
################################################################



# Write your classes here
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
import time
import random
import io
import os.path
import sys


class Block(object):
    """
    Class for blocks
    """
    def __init__(self, dic):
        """
    Initialization method of block class
    reads dictionary and assign values to variables
    Block.__init__(dict) -> None
    """
        self._image = dic['image']
        self._delete = dic['delete']
        self._points = dic['points']
        self._bonus = None
        self._paddle_delta = None
        self._bullets = None
        self._extra_ball = False
        self._clone = False
        if 'bonus' in dic.keys():
            self._bonus = dic['bonus']
        if 'paddle_delta' in dic.keys():
            self._paddle_delta = dic['paddle_delta']
        if 'bullets' in dic.keys():
            self._bullets = dic['bullets']
        if 'extra_ball' in dic.keys():
            self._extra_ball = dic['extra_ball']
        if 'clone' in dic.keys():
            self._clone = dic['clone']

    def get_image(self):
        """
    Returns image name of the block
    Block.get_image() -> Str
    """
        return self._image

    def can_delete(self):
        """
    Returns True if block can be deleted or else false
    Block.can_delete() -> Bool
    """
        if self._delete:
            return True
        else:
            return False

    def get_points(self):
        """
    Returns point value of the block
    also returns bonus points if there is any
    Block.get_points() -> Int
    """
        return self._points

    def get_delta(self):
        """
    Returns paddle delta, 1 or -1
    Block.get_delta() -> Int
    """
        return self._paddle_delta

    def get_bullets(self):
        """
    Returns bullets, not sure what it is
    since only 1 block has blocks value, weird..
    Block.get_bullets() -> Int
    """
        return self._bullets

    def is_bonus(self):
        """
    Returns True or False if block has bonus points or not
    Block.is_bonus() -> Bool
    """
        if self._bonus != None:
            return True
        else:
            return False
    def get_bonus(self):
        """
    retuns bonus points
    Block.get_bonus() -> int"""
        return self._bonus
        
    
    def is_delta(self):
        """
    Returns True or False if block has paddle_delta
    Block.is_delta() -> Bool
    """
        if self._paddle_delta != None:
            return True
        else:
            return False
        
    def is_extra(self):
        """
    Returns True or False value of extra_ball
    Block.is_extra() -> Bool
    """
        return self._extra_ball

    def is_clone(self):
        return self._clone
    
class Paddle(object):
    """Class for paddle object of the game"""
    def __init__(self, cpos):
        """
    Class initialization method
    takes in center position and creates the paddle
    Paddle.__init__(int) -> None
    """
        self._cpos = cpos
        self._height = 10
        self._width = 50
        self._ypos = 440
        

    def get_centre(self):
        """
    Returns centre position of paddle as x,y coordinates
    Paddle.get_centre() -> (int, int)
    """
        return (self._cpos, self._ypos)

    def get_box(self):
        """
    Returns coordinates of the paddles box
    topleft, topright, bottomright, bottomleft
    Paddle.get_box() -> (int, int, int, int)
    """
        self._tlxy = (self._cpos - self._width/2, self._ypos - self._height/2)
        self._trxy = (self._cpos + self._width/2, self._ypos - self._height/2)
        self._brxy = (self._cpos + self._width/2, self._ypos + self._height/2)
        self._blxy = (self._cpos - self._width/2, self._ypos + self._height/2)
        return (int(self._tlxy[0]), int(self._trxy[1]),
                int(self._brxy[0]), int(self._blxy[1]))

    def move(self, position):
        """
    Moves paddle tp desired position
    if position is smaller than 25 or larget than 575
    then it sets a fixed position
    Paddle.move(int) -> None
    """
        maximum = WIDTH - self._width//2
        minimum = 0 + self._width//2
        if position >= maximum:
            self._cpos = maximum
        elif position <= minimum:
            self._cpos = minimum
        else:
            self._cpos = position

class ExtendedPaddle(Paddle):
    """class for extended paddle that inherits from Paddle"""
    def __init__(self, cpos):
        """Initialization method that inherits some variables
    ExtendedPaddle.__init__(int) -> none"""
        super().__init__(cpos)
        self._width = 100

class DecreasedPaddle(Paddle):
    """class for smaller paddle that inherits from Paddle"""
    def __init__(self, cpos):
        """Initialization method that inherits some variables
    DecreasedPaddle.__init__(int) -> none"""
        super().__init__(cpos)
        self._width = 25

class Ball(object):
    """Class for ball object"""
    def __init__(self, x, y):
        """initialization class for the ball object
    takes in x and y coordinates to create the ball and assisngs 0 speed
    Ball.__init__(int, int) -> None
    """
        self._x = x
        self._y = y
        self._sx = 0
        self._sy = 0

    def get_position(self):
        """
    returns position of the ball
    Ball.get_position() -> (int, int)
    """
        return (self._x, self._y)

    def set_position(self, x, y):
        """
    sets the position of the ball
    Ball.set_position(int, int) -> None
    """
        self._x = x
        self._y = y

    def get_speed(self):
        """
    Returns the speed of the ball
    Ball.get_speed() -> (int, int)
    """
        return (self._sx, self._sy)

    def set_speed(self, x, y):
        """
    Changes the speed of the ball
    Ball.set_speed(int, int) -> None
    """
        self._sx = x
        self._sy = y

    def get_y_position(self):
        """
    Returns the y position of the ball
    Ball.get_y_position() -> int
    """
        return self._y
    
    def set_x_position(self, x):
        """
    Changes the x position of ball
    Ball.set_x_position() ->  None
    """
        self._x = x

    def step(self):
        """
    Steps the ball with current ball speed
    ball position x + x.speed, y+ y.speed
    Ball.step() -> None
    """
        self.set_position(self.get_position()[0] + self.get_speed()[0],
                          self.get_position()[1] + self.get_speed()[1])

    
    

class Level(object):
    """Class for game level"""
    def __init__(self, filename):
        """
    Initialization method of level class
    takes in levels filename as argument
    reads the level file and assign values to variables
    Level.__init__(str) -> None
    """
        self._dick = read_level_data(filename)
        self._grid = GridInfo()
        try:
            self._timer = self._dick['timer']
        except KeyError:
            self._timer = 100
        self._filename = filename          
            
        self._blocks = self.blocks()            
        

    def blocks(self):
        """
    internally use method to create blocks for the level
    returns a list with rc coords as tuple and corresponding Blocks
    Level.blocks() -> [[(int, int), Block]]
    """
        coord = []
        dick = []
        blocks = []
        for i in self.get_blocks()[0]:
            coord.append((i[0], i[1]))
        for i in self.get_blocks()[1]:
            dick.append(Block(i))
        for i,x in enumerate(coord):
            blocks.append([coord[i],dick[i]])
        for i in self.create_walls():
            blocks.append([i[0], Block(i[1])])
        return blocks        

    def get_blocks(self):
        """
    internally use method for reading blocks from the level
    it is support method for other internal methods
    Level.get_blocks() -> [[int, int], [dict]]
    """
        blocks = []
        xy = []
        for i in self._dick['blocks']:
            blocks.append(i[1])
            xy.append(i[0])
        return [xy, blocks]

    def block_real_loc_center(self):
        """
    internally use method to translate block locations to xy coords
    used internally for mainly self._blocks variable
    returns the center location of the block so it can be added to gui
    Level.block_real_loc_center() - > [(int, int)]
    """
        loc = []
        loccc = []
        for i in self._blocks:
            loc.append(self._grid.rc2rect(i[0][0], i[0][1]))
        for i in loc:
            x = float(i[0]) + 25
            y = float(i[1]) + 7.5
            loccc.append((x, y))
        return loccc

    def block_rc(self):
        """
    returns the block rowcolumn location as a list
    Level.block_rc() -> [(int, int)]
    """
        loc = []
        locc = []
        for i in self._blocks:
            loc.append((i[0][0], i[0][1]))
        return loc
        

    
    def get_b(self):
        """
    returns the list of blocks
    this method can be called by the model
    Level.get_b() -> [[(int, int), Block]]
    """
        return self._blocks

    def remove_block(self, index):
        """
    removes the selected block from the blocks
    Level.remove_block(int) - > none
    """
        self._blocks.pop(index)

    def get_walls(self):
        """
    Internally used method to read level1.json and
    returns the un-deletable blocks from the file
    Level.get_walls() -> [block*]
    """
        return self.create_walls()
        

    def random_level_generator(self):
        """
    creates random level and saves it to bonus.json
    this function designed for task 4 of the assignment
    Level.random_level_generator -> [[[int, int],{}]*]
    """
        count = 0
        blocks = []

        timer = int((random.random() * 100) + 100)
        
        while count < 48:
            dx = False
            r = int(random.random() * 10)
            c = int(random.random() * 12)
            p = int(random.random() * 10)
            e = int(random.random() * 100)
            clone = int(random.random() * 100)
            d = int(random.random() * 100)
            if p >= 5:
                p = 20
            else:
                p = 10
            if p == 10:
                i = 'red.gif'
            else:
                i = 'bluegreen.gif'
            if e < 10 or e > 90:
                extra = True
            else:
                extra = False
            if clone < 10 or clone > 90 and extra == False:
                cl = True
            else:
                cl = False
            if d < 20 or d > 80:
                if cl == False:
                    if extra == False:
                        if d < 20:
                            delta = -1
                            dx = True
                        else:
                            delta = 1
                            dx = True
            
            if dx:
                block = [[r, c], {"image":i, "delete":True, "points":p,
                              "extra_ball":extra, "clone":cl, "paddle_delta":delta }]
            else:
                block = [[r, c], {"image":i, "delete":True, "points":p,
                              "extra_ball":extra, "clone":cl}]
            blocks.append(block)
            count += 1
        for i in self.get_walls():
            blocks.append(i)

        level = {"timer":timer, "blocks":blocks}
        

        with open('bonus.json', 'w') as file:
                  json.dump(level, file, indent=4)


    def create_walls(self):
        """Method for creating walls as blocks
    these blocks cant be deleted by the game and
    these blocks are invisible on GUI
    Level.create_walls() -> [[[int, int], dict{}]*]"""
        walls = []
        count1 = 0
        count2 = 1
        count3 = 1
        while count1 < 14:
            walls.append([[0, count1], {"image":None, "delete":False, "points":0}])
            count1 += 1

        while count2 < 31:
            walls.append([[count2, 0], {"image":None, "delete":False, "points":0}])
            count2 += 1
        while count3 < 31:
            walls.append([[count3, 13], {"image":None, "delete":False, "points":0}])
            count3 += 1
        return walls
            
        

            
            

class Model(object):
    """Game model class"""
    def __init__(self):
        """
    Initialization method for the class
    Model.__init__() -> None
    """
        self._paddle = Paddle(300)
        self._ball = [Ball(300, 430),]
        self._grid = GridInfo()
        self._col = CollisionHandler(self)
        self._points = 0
        self._bonus = 0
        self._lives = 1
        self._max_lives = 3
        self._alive = True
        self._paddle_is = "normal"
        self._current_ball = 0
        self._current_extra_balls = 0
        self._max_extra_balls = 1

    def update(self):
        """
    Update method for the model, calls in process collusion
    does nothing if no collusion, if collusion, saves the points and
    removes the deletable blocks, also checks if the blocks is special,
    if block speacial like paddle_delta, it increases or decreases the paddle...
    Model.update() -> None
    """
                 
        
        output = []
        
        mainexit = []
        for a, b in enumerate(self._ball):
            self.blockloc = []
            update = self._col.process_collisions()
            self._current_ball = a
            for x in self.get_block_pos():
                self.blockloc.append(x)
            
            if update == []:
                pass
            else:
                for i in update:
                    for c, x in enumerate(self._level.get_b()):
                        if i == x[0]:
                            if x[1].can_delete():
                                self._points += x[1].get_points()
                                if x[1].is_bonus():
                                    self._bonus += x[1].get_bonus()
                                self._level.remove_block(c)
                                output.append(x[0])
                                if x[1].is_extra():
                                    if self._lives != self._max_lives:
                                        self._lives += 1
                                if x[1].is_clone():
                                    if self._current_extra_balls != self._max_extra_balls:
                                        self._ball.append(Ball(self.blockloc[c][0], self.blockloc[c][1]))
                                        self._ball[1].set_speed(BALL_INITIAL_X_SPEED,
                                                            BALL_INITIAL_Y_SPEED)
                                        self._current_extra_balls += 1
                                if x[1].is_delta():
                                    pos = self._paddle._cpos
                                    if x[1].get_delta() == 1:
                                        if self._paddle_is == "normal":
                                            self._paddle = ExtendedPaddle(pos)
                                            self._paddle_is = "big"
                                        elif self._paddle_is == "small":
                                            self._paddle = Paddle(pos)
                                            self._paddle_is = "normal" 
                                        else:
                                            pass
                                    else:
                                        if self._paddle_is == "normal":
                                            self._paddle = DecreasedPaddle(pos)
                                            self._paddle_is = "small"
                                        elif self._paddle_is == "big":
                                            self._paddle = Paddle(pos)
                                            self._paddle_is = "normal"
                                        else:
                                            pass
                                else:
                                    pass
                            else:
                                pass
        return output

    def level_timer(self):
        """
    Returns level timer
    Model.level_timer() -> int
    """
        return self._level._timer
    

    def get_ball_position(self):
        """
    returns the position of the ball
    Model.get_ball_position() -> (int, int)
    """
        try:
            return self._ball[self.which_ball()].get_position()
        except:
            return self._ball[0].get_speed()

    def get_ball_speed(self):
        """
    Returns the ball speed
    Model.get_ball_speed() -> (int, int)
    """
        try:
            return self._ball[self.which_ball()].get_speed()
        except:
            return self._ball[0].get_speed()

    def set_ball_position(self, x, y):
        """
    sets the ball position
    Model.set_ball_position(int, int) -> none
    """
        try:
            self._ball[self.which_ball()].set_position(x, y)
        except:
            self._ball[0].set_position(x, y)

    def set_ball_speed(self, sx, sy):
        """
    sets the ball speed
    Model.set_ball_speed(int, int) -> none
    """
        try:
            self._ball[self.which_ball()].set_speed(sx, sy)
        except:
            self._ball[0].set_speed(sx, sy)

    def is_block_at(self, cp):
        """
    checks if there is a block at the row columng
    Model.is_block_at([int, int]) -> Bool
    """
        block_rc = self._level.block_rc()
        if cp in block_rc:
            return True
        else:
            return False

    def get_paddle_box(self):
        """
    Returns paddle box area
    Model.get_paddle_box() -> [int, int, int, int]
    """
        return self._paddle.get_box()

    def get_paddle_center(self):
        """
    returns centre location of the paddle
    Model.get_paddle_center() -> int
    """
        return self._paddle.get_centre()

    def exit_ball(self):
        """
    removes the ball from the game
    Model.exit_ball() -> none
    """ 
        mainballspeed = self._ball[0].get_speed()
        mainballpos = self._ball[0].get_position()
        try:
            if self._lives != 0 and self._current_ball == 0:
                self._ball.pop(0)
                self._paddle = Paddle(300)
                self._ball = [Ball(300, 430),]
                self._lives -= 1
            elif self._lives != 0 and self._current_ball == 1:
                self._ball.pop(1)
                self._current_extra_balls = 0
                self._current_ball = 0
            else:
                self._alive = False
                
        except IndexError:
            self._paddle = Paddle(300)
            self._ball = [Ball(300, 430),]
            self._current_extra_balls = 0
            self._current_ball = 0

            
    def step_ball(self):
        """
    calls in step ball function
    Model.step_ball() -> none
    """
        self._ball[self.which_ball()].step()

    def move_paddle(self, cx):
        """
    moves the paddle
    model.Move(int) - > none
    """
        self._paddle.move(cx)

    def ball_move(self, cx):
        """
    moves the ball to designated x position
    Model.ball_move(int) - > none
    """
        self._ball[self.which_ball()].set_x_position(cx)

    def get_ball_y(self):
        """
    returns ball y positions
    Model.get_ball_y() -> int
    """
        
        return self._ball[self.which_ball()].get_y_position()

    def get_blocks(self):
        """
    returns blocks list
    Model.get_blocks() -> [blocks]
    """
        return self._level.get_b()

    def get_block_pos(self):
        """
    returns block posiitons
    Model.get_block_pos() - > [int *]
    """
        return self._level.block_real_loc_center()

    def set_ball_position(self, x, y):
        """
    sets ball position
    Model.set_ball_position(int, int) -> none
    """
        
        self._ball[self.which_ball()].set_position(x, y)

    def status_check(self):
        """
    checks if there are any removable blocks left in the game
    Model.status_check() -> Bool
    """
        status = []
        for i,x in self._level.get_b():
            if x.can_delete():
                status.append(x)
        if len(status) > 0:
            return False
        else:
            return True

    def load_level(self, level):
        """
    loads new level for the model
    Model.load_level(json) -> none
    """
        self._level = Level(level)
        self._paddle = Paddle(300)
        self._ball = [Ball(300, 430),]
        self._current_ball = 0
        self._max_extra_balls = 1
        self._alive = True

    def which_ball(self):
        """
    Internal function to tell the model which ball to move
    Model.which_ball() - > Int """
        return self._current_ball


    def specific_ball_position(self, index):
        """Returns ball position for specific ball
    Model.specific_ball_position(int) -> (int, int)"""
        return self._ball[index].get_position()
        

        
            
        
        

# Write your GUI instantiation code here

    
class Status(tk.Frame):
    """Status bar widget"""
    def __init__(self, master, parent):
        """Initiazlization method
    inherits from tk.Frame as its master widget and takes argument parent widget
    Status.__init__(GUIMasterWidget) -> none"""
        super().__init__(master)
        self._parent = parent
        self._lives = 1
        

        self.customFont = font.Font(family='Impact', size=10)
        

        self.point_label = tk.Label(self, text='0', width = 5,
                                    font = self.customFont, fg='red', bg='black')
        self.point_label.pack(side=tk.RIGHT, fill=tk.X, padx=10)
        self.writing = tk.Label (self, text='Score', font=self.customFont,
                                 fg='red')
        self.writing.pack(side=tk.RIGHT)


        self.level_label = tk.Label(self, text='Level 1', font=self.customFont,
                                    fg='red')
        self.level_label.pack(side=tk.RIGHT, padx=100)

        self.timer_label = tk.Label(self, text='0', width = 5,
                            font =self.customFont, fg='yellow', bg='black')
        self.timer_label.pack(side=tk.RIGHT)

        self.writing = tk.Label (self, text='Timer', font=self.customFont,
                                 fg='blue')
        self.writing.pack(side=tk.RIGHT)

        self.ball_image = tk.PhotoImage(file = 'ball.gif')
        self.ball_labels= []
        self.ball_labels.append(tk.Label(self, image = self.ball_image))
        self.ball_labels[0].pack(side=tk.RIGHT)
        self.ball_labels.append(tk.Label(self, image = self.ball_image))
        self.ball_labels[1].pack(side=tk.RIGHT)
        self.ball_labels.append(tk.Label(self, image = self.ball_image))
        self.ball_labels.append(tk.Label(self, image = self.ball_image))

        self.but2 = tk.Button(self, text='CHEAT', fg ='blue',
                              command=self.cheat)
        self.but2.pack(side=tk.LEFT, padx=5)

        self.but3 = tk.Button(self, text='Random Level', fg='green',
                              command=self.random_level)
        self.but3.pack(side=tk.LEFT, padx=5)

        self.lives = 1

    def remove_ball(self, index):
        """removes ball gif
    Status.remove_ball() -> none"""
        try:
            self.ball_labels[index].pack_forget()
        except:
            pass

    

    def add_ball(self, index):
        """adding back the ball packs
    Status.add_balls() -> none"""
        self.ball_labels[index].pack(side=tk.RIGHT)

       

    def update_points(self, value):
        """
    Updates the points in the status bar
    Status.updete_points(Int/Str) -> None"""
        self.point_label.configure(text="{0}".format(value))

    def update_timer(self, value):
        """
    Updates the timer in the status bar
    Status.updete_points(Int/Str) -> None"""
        self.timer_label.configure(text="{0}".format(value))

    def update_level(self, value):
        """
    Updates the level information on the status bar
    Status.update_level(STR) -> None"""
        self.level_label.configure(text="Level {0}".format(value))

    def restart(self):
        """
    Calls parents restart method to restart the game
    Status.restart() -> none"""
        self._parent.restart()
        
    def cheat(self):
        """Calls in parents cheat method
    Status.cheat() -> None"""
        self._parent.cheat()

    def random_level(self):
        """Calls in parents random level method
    Status.random_level()"""
        self._parent.random_level()


class Breakout(object):
    """TOP LEVEL GUI CLASS
    Inherits from objec, its designed to be top level gui
    its master should be tk.root itself"""
    def __init__(self, master):
        """Initiazlization method for the gui
    Breakout.__init__(tk) -> none"""
        self._master = master
        self._points = 0
        self._bonus = True
        self._model_count = 0
        self._game = True
        self._at_level = 0
        self._lives = 1
        self.ball = []
        self._number_of_levels = len(read_level_data('levels.json'))
        self._levels = read_level_data('levels.json')
        self._start_time = time.time()
        
        master.title('Assignment 3 - Breakout Game - Arda Akgur')
        
        self._model = Model()
        self.status_bar = Status(master, self)
        self.status_bar.pack(expand=1, fill=tk.X, padx=20)
        self.start(self._levels[0])
        
        
        self._canvas = tk.Canvas(master, bg='black',
                                 width=WIDTH, height=HEIGHT)
        self._canvas.pack(expand=1, padx=20, pady=20)

        self._canvas.bind("<Motion>", self.motion)
        self._canvas.bind("<Button-1>", self.button1)
        self._canvas.bind("<Leave>", self.leave)
        self._canvas.bind("<Enter>", self.enter)
        self.images = {
            "ball.gif" : tk.PhotoImage(file = 'ball.gif'),
            "paddle.gif" : tk.PhotoImage(file = 'paddle.gif'),
            "red.gif" : tk.PhotoImage(file= 'red.gif'),
            "bluegreen.gif": tk.PhotoImage(file= 'bluegreen.gif'),
            "increase_paddle.gif": tk.PhotoImage(file= 'increase_paddle.gif'),
            "decrease_paddle.gif": tk.PhotoImage(file= 'decrease_paddle.gif'),
            "ball2.gif": tk.PhotoImage(file = 'ball2.gif')
        }

        menubar = tk.Menu(master)
        master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        helpmenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        filemenu.add_command(label="New Game", command=self.restart)
        filemenu.add_command(label="Load Custom Level", command=self.load)
        filemenu.add_command(label="High Scores", command=self.highscore)
        filemenu.add_command(label="Exit", command=self.exit)
        helpmenu.add_command(label="About", command=self.about)
        
        

        self._game_running = True
        
        
        self.ready()
        
        

    def highscore(self):
        """Checks if there is highscores.txt, if there is then shows the content,
    if there is no highscores.txt, it creates a new one with placeholder highscore list
    Breakout.highscore() -> messagebox(str)"""
        if os.path.exists('highscores.txt'):
            file = open('highscores.txt', 'r')
            data = []
            for line in file:
                line = line.strip()
                data.append(line)
            messagebox.showinfo("High Scores",
                "{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(data[0],
                data[1], data[2], data[3], data[4], data[5]))
            file.close()
        else:
            file = open('highscores.txt', 'w')
            information = ['Player1 60',
                           'Player2 50',
                           'Player3 40',
                           'Player4 30',
                           'Player5 20',
                           'Player6 10']
            file.write(information[0] +'\n')
            file.write(information[1] +'\n')
            file.write(information[2] +'\n')
            file.write(information[3] +'\n')
            file.write(information[4] +'\n')
            file.write(information[5] +'\n')
            file.close()
            self.highscore()
            

    def about(self):
        """simple about method to show info about the software
    Breakout.about() -> messagebox(str)"""
        messagebox.showinfo("About Breakout",
            "This program written by \nArda 'Arc' Akgur\n for CSSE1001 Assignment3")

    def load(self, filename=None):
        """In order to load custom levels
    Breakout.load(filename.json) ->none"""
        if not filename:
            filename = filedialog. \
                askopenfilename(initialdir=os.getcwd(),
                                title="Data File",
                                filetypes=(("json files", "*.json"),))
        if filename:
            self._game = True
            self._lives = 1
            self._model._alive = True
            self._model._lives = 1
            self.start(filename)
            
            
            
    
    def redraw(self):
        """Deletes canvas and adds every object to the game
    this method reads the Model class and learns about the object positions
    Breakout.redraw() -> none"""
        self._canvas.delete(tk.ALL)
        try:
            for i,x in enumerate(self._model._ball):
                if i == 0:
                    self._canvas.create_image(self._model.specific_ball_position(i)[0],
                                    self._model.specific_ball_position(i)[1],
                                    image = self.images["ball.gif"])
                elif i == 1:
                    self._canvas.create_image(self._model.specific_ball_position(i)[0],
                                    self._model.specific_ball_position(i)[1],
                                    image = self.images["ball2.gif"])
        except IndexError:
            pass
        self.paddle = self._canvas.create_rectangle(*self._model.get_paddle_box(), fill = "blue")
        self.blockloc = {}
        for i, x in enumerate(self._model.get_block_pos()):
            self.blockloc[i] = x

        self.blocks = []
        for i in self._model.get_blocks():
            self.blocks.append(i[1])

        for i,x in enumerate(self.blockloc):
            try:
                self._canvas.create_image(self.blockloc[x][0], self.blockloc[x][1],
                            image = self.images[self.blocks[i].get_image()])
                if self.blocks[i].is_extra():
                    self._canvas.create_image(self.blockloc[x][0], self.blockloc[x][1],
                            image = self.images["ball.gif"])
                if self.blocks[i].is_delta():
                    if self.blocks[i].get_delta() == 1:
                        self._canvas.create_image(self.blockloc[x][0], self.blockloc[x][1],
                            image = self.images["increase_paddle.gif"])
                    else:
                        self._canvas.create_image(self.blockloc[x][0], self.blockloc[x][1],
                            image = self.images["decrease_paddle.gif"])
                if self.blocks[i].is_clone():
                    self._canvas.create_image(self.blockloc[x][0], self.blockloc[x][1],
                            image = self.images["ball2.gif"])
                        
            except KeyError:
                pass
    
    def motion(self, e):
        """Method for moving the game paddle
    it requires game to be active
    Breakout.motion(event) - > none"""
        if self._game:
            try:
                if self._model.get_ball_speed() == (0, 0):
                    self._model.move_paddle(e.x)
                    x, y = self._model.get_paddle_center()
                    self._model.ball_move(x)
                    self.redraw()
                else:
                    self._model.move_paddle(e.x)
                    self.redraw()
            except IndexError:
                pass
            
            

    def button1(self, e):
        """Method for moust button 1 click
    it checks if game is active and if ball speed is 0,0
    then it changes ball speed
    Breakout.button1(Event) ->none"""
        print("Model {}".format(self._model._id))
        if self._game:
            if self._model.get_ball_speed() == (0, 0):
                self._model.set_ball_speed(BALL_INITIAL_X_SPEED, BALL_INITIAL_Y_SPEED)
                self._start_time = time.time()
                self._timer = self._model.level_timer()
                self.status_bar.update_timer(self._timer)
            else:
                pass
        else:
            pass

        

    def update(self):
        """Update function that is using models update and checks few things
    first if mouse is not in the canvas, it pauses the game
    secondly it checks if game is active and tries Model.update(), if model update fails
    then exits the ball since model update would only fail because of the support code and
    only way to prevent that error is exiting ball
    thirdly it updates points of the gui if there was point update in model
    forthly it calls itself again
    in the meantime this method also checks if level is complete
    also it checks if the player has enough lives to continue the game
    Breakout.update() -> none"""
        current_time = time.time()
        
        if not self._game_running:
            self.ready()
            return
        
        if self._game:
            try:
                self._model.update()
            except:
                self._model.exit_ball()
            self.status_bar.update_points(self._model._points)
            self._points = self._model._points               
            self.ready()
            if self._model._lives > self._lives:
                self._lives = self._model._lives
                self.status_bar.add_ball(self._lives)
            elif self._model._lives < self._lives:
                self.status_bar.remove_ball(self._lives)
                self._lives = self._model._lives
            if self._model._alive == False:
                self._master.after_cancel(self.test)
                self._game = False
                messagebox.showinfo("GAME OVER!",
                                    "Bad luck mate!\nMaybe better luck next time!")
                self.check_score_worthy(self._points)
            try:
                if self._model.get_ball_speed() != (0, 0):
                    if current_time - self._start_time > 1:
                        self._timer -= 1
                        self.status_bar.update_timer(self._timer)
                        self._start_time = time.time()
                        if self._timer == 0:
                            self._bonus = False
            except:
                pass
            if self._model.status_check():
                try:
                    if self._bonus:
                        self._points += self._model._bonus
                    self._at_level += 1
                    self.start(self._levels[self._at_level])
                    self.status_bar.update_level(self._at_level + 1)
                    self._timer = self._model.level_timer()
                    self.status_bar.update_timer(self._timer)
                    self._start_time = time.time()
                except:
                    self._master.after_cancel(self.test)
                    self._game = False
                    messagebox.showinfo("Congratulations!!", "GAME OVER!")
                    self.check_score_worthy(self._points)

    def start(self, level):
        """Main method to start a level
    it takes level as argument, level argument given from Breakout.update()
    Breakout.start(str) -> none"""

        self._model.load_level(level)
        self._model._paddle = Paddle(300)
        self._model._ball[0] = Ball(300, 430)
        self._timer = -1
        self.status_bar.update_timer(0)
        self._model._points = self._points
        self._model_count += 1
        self._model._id = self._model_count
        self._game = True
        self._lives = 1
        self._model._lives = 1
        self._model._alive = True

    def leave(self, event):
        """method for pausing the game
    Breakout.leave(event) -> none"""
        self._game_running = False

    def enter(self, event):
        """method for unpausing the game
    Breakout.enter(event) -> none"""
        self._game_running = True
       

    def ready(self):
        """After method to keep the update() going
    update calls ready, ready calls update
    Breakout.ready() -> none"""
        self.redraw()
        self.test = self._master.after(TIME_STEP, self.update)

    def restart(self):
        """Restart method to start a new game from beginning, it resets most
    but it keeps a counter for debugging purposes
    Breakout.restart() -> none"""
        self._lives = 1
        self.status_bar.pack_forget()
        self._canvas.pack_forget()
        self._master.after_cancel(self.test)
        self._model = Model()
        self._model.load_level(self._levels[0])
        self._model_count += 1
        self._model._id = self._model_count
        self._points = 0
        self._bonus = True
        self._level_at = 0
        self.status_bar = None
        self.status_bar = Status(self._master, self)
        self.status_bar.pack(expand=1, fill=tk.X, padx=20)
        self._canvas = tk.Canvas(self._master, bg='black',
                                 width=WIDTH, height=HEIGHT)
        self._canvas.pack(expand=1, padx=20, pady=20)

        self._canvas.bind("<Motion>", self.motion)
        self._canvas.bind("<Button-1>", self.button1)
        self._canvas.bind("<Leave>", self.leave)
        self._canvas.bind("<Enter>", self.enter)
        self.images = {
            "ball.gif" : tk.PhotoImage(file = 'ball.gif'),
            "paddle.gif" : tk.PhotoImage(file = 'paddle.gif'),
            "red.gif" : tk.PhotoImage(file= 'red.gif'),
            "bluegreen.gif": tk.PhotoImage(file= 'bluegreen.gif'),
            "increase_paddle.gif": tk.PhotoImage(file= 'increase_paddle.gif'),
            "decrease_paddle.gif": tk.PhotoImage(file= 'decrease_paddle.gif'),
            "ball2.gif": tk.PhotoImage(file = 'ball2.gif')
        }
        self.status_bar.update_level(1)
        self._game = True
        self._timer = -1
        self.status_bar.update_timer(0)
        self.ready()

    def cheat(self):
        """Cheat method for lazy people,
    it destroys some of the blocks in the game
    Breakout.cheat() -> none """
        for c, x in enumerate(self._model._level.get_b()):
            if x[1].can_delete():
                self._model._level.remove_block(c)

    def random_level(self):
        """Method for starting a random level...
    calls the level classes random level generator
    starts the random level
    Breakout.random_level() ->"""
        self._master.after_cancel(self.test)
        self._model._level.random_level_generator()
        self._points = 0
        self._bonus = True
        self._level_at = 100
        self.status_bar.update_level('X')
        self._model._current_extra_balls = 0
        self._model._current_ball = 0
        self._model._alive = True
        self._model._lives = 1
        self._lives = 1
        self.start('bonus.json')
        self.ready()
        

    def check_score_worthy(self, score):
        """Method for checking if player score is worthy enough to be in the
    highscore list, first checks if there is even a highscore list, if not
    it creates one and then checks that list.. if player is worthy, asks name
    then adds the player name and score to the list and saves it in a file
    Breakout.check_score_worthy(int) -> filesave or no filesave, depends of score"""
        if os.path.exists('highscores.txt'):
            try:
                file = open('highscores.txt', 'r')
                data = []
                for line in file:
                    line = line.strip()
                    data.append(line)
                self._data = data
                for i, x in enumerate(data):
                    if int(x.split(' ')[1]) < score:
                        self._score_position = i
                        break
                file.close()
                self._data.insert(self._score_position,
                                  str(tk.simpledialog.askstring("Your Name", "Your nick\n please no spaces")) + ' ' +str(self._points))
                
                for i,x in enumerate(self._data[:6]):
                    if len(x) < 5:
                        self._data[i] = 'NoName ' + x
                file = open('highscores.txt', 'w')
                information = self._data[:6]
                file.write(information[0] +'\n')
                file.write(information[1] +'\n')
                file.write(information[2] +'\n')
                file.write(information[3] +'\n')
                file.write(information[4] +'\n')
                file.write(information[5] +'\n')
                file.close()
                self.highscore()
            except:
                self.highscore()
            
            
            
        else:
            file = open('highscores.txt', 'w')
            information = ['Player1 60',
                           'Player2 50',
                           'Player3 40',
                           'Player4 30',
                           'Player5 20',
                           'Player6 10']
            file.write(information[0] +'\n')
            file.write(information[1] +'\n')
            file.write(information[2] +'\n')
            file.write(information[3] +'\n')
            file.write(information[4] +'\n')
            file.write(information[5] +'\n')
            file.close()
            self.check_score_worthy(self._points)
        
        
    def exit(self):
        """exitsgame
    Breakout.exit() - > bye bye"""
        self._master.destroy()
        
        
    


def main():
    root = tk.Tk()
    app = Breakout(root)
    root.mainloop()
################################################################
# Write your code above - NOTE you should define a top-level
# class (the application) called Breakout
################################################################
if __name__ == '__main__':
    main()
