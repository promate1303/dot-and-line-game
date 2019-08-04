from tkinter import *
import tkinter.messagebox
import sys

n111=0

def about2():
    ab = Toplevel()
    ab1 = Label(ab,  text="Dots and Boxes is a pencil-and-paper game for \n two players.It was first published"
                          " in the 19th century\n by French mathematician Édouard Lucas, who called it "
                          "la pipopipette.\n It has gone by many other names, including the game of dots,"
                          "\n dot to dot grid, boxes, and pigs in a pen.", bg="KHAKI2", bd=100, relief=RIDGE)
    ab1.config(font=("Courier", 20))
    ab1.pack()
def help2():
    he = Toplevel()
    h2 = Label(he, text="The game is played starting with a rectangular array\n of dots.The two players take turns to "
                        "join two adjacent\n dots with a horizontal or vertical line. If a player completes \n the fourth "
                        "side of a box they initial that box and must draw another \nline. When all the boxes have been"
                        " completed the winner is the player\n who has initialled the most boxes.The game is more complex"
                        " \nthan it initially appears, and even on a 4x4 grid there is \nplenty of opportunity for skilful"
                        " play.", bg="KHAKI2", bd=100, relief=RIDGE)

    h2.config(font=("Courier", 20))
    h2.pack()

def new1():
    global n111
    n111 = 1
def new2():
    global n111
    n111 = 2
def new3():
    global n111
    n111 = 3
def new4():
    global n111
    n111 = 4
def new5():
    global n111
    n111 = 5
def new6():
    global n111
    n111 = 6
def new7():
    global n111
    n111 = 7
def new8():
    global n111
    n111 = 8
def new9():
    global n111
    n111 = 9
def new10():
    global n111
    n111 = 10

switch = {1:new1,2:new2,3:new3,4:new4,5:new5,6:new6,7:new7,8:new8,9:new9,10:new10}

def new_window():                                     #GAME WINDOW:
    top= Toplevel()
    TOL = 10
    CELLSIZE = 50
    OFFSET = 30
    CIRCLERAD = 5
    DOTOFFSET = OFFSET + CIRCLERAD
    GAME_H = 500
    GAME_W = 500

    class Player(object):
        def __init__(self, name, color="yellow"):
            self.score = 0
            self.str = StringVar()
            self.name = name
            self.color = color
        def update(self):
            self.str.set(self.name + ": %d" % self.score)

    class MyFrame(Frame) :
        def __init__(self, master):
            Frame.__init__(self, master)
            self.canvas = Canvas(self, height = GAME_H, width = GAME_W,bg="khaki2")
            self.canvas.bind("<Button-1>", lambda e:self.click(e))		#binds to  button1 of mouse
            self.canvas.grid(row=1,column=0)
            self.dots = [[self.canvas.create_oval(CELLSIZE*i+OFFSET, \
                                                  CELLSIZE*j+OFFSET, \
                                                  CELLSIZE*i+OFFSET+2*CIRCLERAD, \
                                                  CELLSIZE*j+OFFSET+2*CIRCLERAD, \
                                                  fill="green2") \
                          for j in range(n111)] for i in range(n111)]
            self.lines = []
            self.infoframe = Frame(self)		#Score Card
            self.players = [Player("1st","blue"), Player("2nd","red")] #initialize player1 and 2nd
            self.infoframe.players = [Label(self.infoframe, textvariable = i.str,bg="plum2",height=2,width=62) for i in self.players]
            for i in self.infoframe.players:
                i.grid()
            self.turn = self.players[0]
            self.update_players()
            self.infoframe.grid(row =0, column = 0, sticky = N)
            self.grid()
        def update_players(self):
            for i in self.players:
                i.update()
        def click(self, event):
            x,y = event.x, event.y
            orient = self.isclose(x,y)
            if orient:
                if self.line_exists(x,y, orient):
                    return
                l = self.create_line(x,y, orient)
                score = self.new_box_made(l)
                if score:
                    self.turn.score += score
                    self.turn.update()
                    self.check_game_over()
                else:
                    index = self.players.index(self.turn)
                    self.turn = self.players[1-index]
                self.lines.append(l)
        def create_line(self, x, y, orient):
            startx = CELLSIZE * ((x-OFFSET)//CELLSIZE) + DOTOFFSET
            starty = CELLSIZE * ((y-OFFSET)//CELLSIZE) + DOTOFFSET
            tmpx = (x-OFFSET)//CELLSIZE
            tmpy = (y-OFFSET)//CELLSIZE

            if orient == HORIZONTAL:
                endx = startx + CELLSIZE
                endy = starty
            else:
                endx = startx
                endy = starty + CELLSIZE
            #print "line drawn: %d,%d to %d,%d" % (startx,starty,endx,endy)
            return self.canvas.create_line(startx,starty,endx,endy,fill="gray1")

        def new_box_made(self, line):
            score = 0
            x0,y0,x1,y1 = self.canvas.coords(line)
            if x0 == x1: # vertical line
                midx = x0
                midy = (y0+y1)/2
                pre = (x0 - CELLSIZE/2, midy)
                post = (x0 + CELLSIZE/2, midy)
            elif y0 == y1: # horizontal line
                midx = (x0 + x1)/2
                midy = y0
                pre = (midx, y0 - CELLSIZE/2)
                post = (midx, y0 + CELLSIZE/2)

            if len(self.find_lines(pre)) == 3:  # not 4, because newly created line is
                self.fill_in(pre)               # is not returned (?!)
                score += 1
            if len(self.find_lines(post)) == 3:
                self.fill_in(post)
                score += 1
            return score
        def find_lines(self, coords):
            x, y = coords
            if x < 0 or x > GAME_W:
                return []
            if y < 0 or y > GAME_W:
                return []
            #print "Cell center: %d,%d" % (x,y)
            lines = [x for x in self.canvas.find_enclosed(x-CELLSIZE, \
                                                          y-CELLSIZE, \
                                                          x+CELLSIZE, \
                                                          y+CELLSIZE) \
                     if x in self.lines]
            #print lines
            return lines
        def fill_in(self, coords):
            x,y = coords
            self.canvas.create_text(x,y,text=self.turn.name, fill=self.turn.color)

        def isclose(self, x, y):
            x -= OFFSET
            y -= OFFSET
            dx = x - (x//CELLSIZE)*CELLSIZE
            dy = y - (y//CELLSIZE)*CELLSIZE

            if abs(dx) < TOL:
                if abs(dy) < TOL:
                    return None                       # mouse in corner of box; ignore
                else:
                    return VERTICAL
            elif abs(dy) < TOL:
                return HORIZONTAL
            else:
                return None
        def line_exists(self, x,y, orient):
            id_ = self.canvas.find_closest(x,y,halo=TOL)[0]
            if id_ in self.lines:
                return True
            else:
                return False
        def check_game_over(self):
            total = sum([x.score for x in self.players])
            if total == (n111-1)*(n111-1):
                if self.players[0].score > self.players[1].score:
                    tkinter.messagebox.showwarning(
                        title = "GAME OVER",
                        message ="Winner is Player1\n Player1 :%3d\n Player2: %3d\t"% (
                            self.players[0].score,self.players[1].score)
                    )
                elif self.players[0].score == self.players[1].score:
                    tkinter.messagebox.showwarning(
                        title = "GAME OVER",
                        message ="Match is Draw\n Player1 :%3d\n Player2: %3d\t"% (
                            self.players[0].score,self.players[1].score)
                    )

                else:
                    tkinter.messagebox.showwarning(
                        title = "GAME OVER",
                        message ="Winner is Player2\nPlayer1 :%3d\n Player2: %3d\t"% (
                            self.players[0].score,self.players[1].score)
                    )
                sys.exit(0)
    top.f = MyFrame(top)

class Man:                                         #MAIN WINDOW:
    root = Tk()
    root.configure(bg="CORAL2")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  #Full screen


    # Message box
    tkinter.messagebox.showinfo("Welcome message","Hola,welcome friends to the DOT AND LINE GAME")

    # Menubar options
    menu = Menu(root)
    root.config(menu=menu)

    single_player_menu = Menu(menu)
    menu.add_cascade(label="MATRIX SIZE",menu=single_player_menu)
    single_player_menu.add_command(label="1x1", command=switch.get(1))
    single_player_menu.add_command(label="2x2", command=switch.get(2))
    single_player_menu.add_command(label="3x3", command=switch.get(3))
    single_player_menu.add_command(label="4x4", command=switch.get(4))
    single_player_menu.add_command(label="5x5", command=switch.get(5))
    single_player_menu.add_separator()
    single_player_menu.add_command(label="6x6", command=switch.get(6))
    single_player_menu.add_command(label="7x7", command=switch.get(7))
    single_player_menu.add_command(label="8x8", command=switch.get(8))
    single_player_menu.add_command(label="9x9", command=switch.get(9))
    single_player_menu.add_command(label="10x10", command=switch.get(10))

    help1 = Menu(menu)
    menu.add_cascade(label="Help?", menu=help1)
    help1.add_command(label="info", command=help2)

    about = Menu(menu)
    menu.add_cascade(label="About",menu=about)
    about.add_command(label="info", command=about2)

    start = Button(root, text='START', height=5, width=50, command=new_window, activebackground="GRAY26",
                   activeforeground="AQUAMARINE",
                   bd=20, bg="WHEAT1", relief=GROOVE)
    start.pack(side="top", expand=True, padx=4, pady=4)


    root.mainloop()

m = Man()