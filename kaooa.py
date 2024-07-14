from turtle import *
from shapely.geometry import LineString
import time

TOTAL_CROWS = 7
TARGET_CROWS = 4
hideturtle()
t = Turtle()
t.pensize(3)
t.speed(0)
t.hideturtle()
# t.screen.bgcolor("orange")
SIDE_LENGTH = 500
no_crows = 0
prev_crow_idx = 0
no_crows_captured = 0 
CROW_COLOR = "red"
VULTURE_COLOR = "yellow"

class Spot():
    def __init__(self,x,y,index,color="white") -> None:
        self.x = x
        self.y = y
        self.radius = 25
        self.color = color
        self.is_empty = True
        self.reachable_spots = []
        self.index = index
        self.capturable_spots = []
    
    def assign(self,pos):
        self.x = pos[0]
        self.y = pos[1]
    
    def __str__(self) -> str:
        return f"[{self.x},{self.y}]"

    def draw_circle(self):
        t.penup()
        t.goto(self.x, self.y)
        t.color("black", self.color)
        t.forward(self.radius)
        t.left(90)
        t.pendown()
        t.begin_fill()
        t.circle(self.radius)
        t.end_fill()

vulture_prevloc = Spot(0,0,-1)
vulture_prevloc.reachable_spots = [1,2,3,4,5,6,7,8,9,10]
prev_spot = Spot(0,0,-1)
# class Crow():


I1 = Spot(0,0,1)
I2 = Spot(0,0,2)
I3 = Spot(0,0,3)
I4 = Spot(0,0,4)
I5 = Spot(0,0,5)
I6 = Spot(0,0,6)
I7 = Spot(0,0,7)
I8 = Spot(0,0,8)
I9 = Spot(0,0,9)
I10 = Spot(0,0,10)
I1.reachable_spots = [3,4]
I2.reachable_spots = [3,6]
I3.reachable_spots = [1,2,4,6]
I4.reachable_spots = [1,3,5,7]
I5.reachable_spots = [4,7]
I6.reachable_spots = [2,3,8,9]
I7.reachable_spots = [4,5,8,10]
I8.reachable_spots = [6,7,9,10]
I9.reachable_spots = [6,8]
I10.reachable_spots = [7,8]
I1.capturable_spots = [6,7]
I2.capturable_spots = [4,8]
I3.capturable_spots = [5,9]
I4.capturable_spots = [2,10]
I5.capturable_spots = [3,8]
I6.capturable_spots = [1,10]
I7.capturable_spots = [1,9]
I8.capturable_spots = [2,5]
I9.capturable_spots = [3,7]
I10.capturable_spots = [4,6]

def find_intersection(line1, line2):
    intersection = line1.intersection(line2)
    return intersection.x, intersection.y

def draw_circle(centre,radius,color):
    t.penup()
    t.goto(centre.x,centre.y)
    t.color("black",color)
    t.forward(radius)
    t.left(90)
    t.pendown()
    t.begin_fill()
    t.circle(radius)
    t.end_fill()


def draw_star():
    t.penup()
    t.goto(-170,-170)
    I9.assign(t.pos())
    t.pendown()
    t.left(72)
    t.fd(SIDE_LENGTH)
    I1.assign(t.pos())
    t.right(180-36)
    t.fd(SIDE_LENGTH)
    I10.assign(t.pos())
    t.right(180-36)
    t.fd(SIDE_LENGTH)
    I2.assign(t.pos())
    t.right(180-36)
    t.fd(SIDE_LENGTH)
    I5.assign(t.pos())
    t.right(180-36)
    t.fd(SIDE_LENGTH)
    line1 = LineString([(I9.x,I9.y),(I1.x,I1.y)])
    line2 = LineString([(I1.x,I1.y),(I10.x,I10.y)])
    line3 = LineString([(I10.x,I10.y),(I2.x,I2.y)])
    line4 = LineString([(I2.x,I2.y),(I5.x,I5.y)])
    line5 = LineString([(I5.x,I5.y),(I9.x,I9.y)])
    I3.x, I3.y = find_intersection(line1,line4)
    I4.x, I4.y = find_intersection(line2,line4)
    I6.x, I6.y = find_intersection(line1,line3)
    I7.x, I7.y = find_intersection(line2,line5)
    I8.x, I8.y = find_intersection(line3,line5)
    

def check_move(spot_list,idx):
    for index in spot_list[idx-1].reachable_spots:
        if spot_list[index-1].is_empty:
            return True
    
    return False

def check_capture(spot_list,idx):
    for index in spot_list[idx-1].capturable_spots:
        if spot_list[index-1].is_empty:
            return True
    
    return False


def crow_turn1(x, y):
    global no_crows
    global prev_crow_idx
    global prev_spot
    flag = -1
    for spot in spot_list:
        distance = ((x - spot.x) ** 2 + (y - spot.y) ** 2) ** 0.5
        if distance <= spot.radius:
            if no_crows < TOTAL_CROWS and spot.is_empty:
                spot.color = CROW_COLOR
                flag = 1
                spot.is_empty = False
                no_crows += 1
            elif no_crows >= TOTAL_CROWS and not spot.is_empty:
                if check_move(spot_list,spot.index):
                    spot.color = "white"
                    prev_crow_idx = spot.index
                    prev_spot = spot
                    spot.is_empty = True
                    flag = 0
                else:
                    print("This Crow doesn't have a valid move")
                    flag = 2
            elif no_crows < TOTAL_CROWS and not spot.is_empty:
                print("Click on a valid spot")
                flag = 2
                # t.getscreen().onscreenclick(crow_turn1)
            elif no_crows >= TOTAL_CROWS and spot.is_empty:
                print("Select a Crow first")
                flag = 2
                # t.getscreen().onscreenclick(crow_turn1)

            clear()
            spot.draw_circle()
    if flag == 1:
        if check_move(spot_list,vulture_prevloc.index) or check_capture(spot_list,vulture_prevloc.index):
            t.getscreen().onscreenclick(vulture_turn)
        else:
            print("Crow Win")
            crow_win_text = "Crows Win!!"
            t.penup()
            t.goto(0, window_height() / 2 - 60)
            t.pendown()
            t.color(CROW_COLOR)
            t.write(crow_win_text,align="center",font=("Arial", 46, "normal"))
            time.sleep(3)
            Screen().bye()
            return
    elif flag == 0:
        t.getscreen().onscreenclick(crow_turn2)
    elif flag == 2:
        t.getscreen().onscreenclick(crow_turn1)

def crow_turn2(x, y):
    flag = -1
    for spot in spot_list:
        distance = ((x - spot.x) ** 2 + (y - spot.y) ** 2) ** 0.5
        if distance <= spot.radius:
            if spot.is_empty and spot.index in prev_spot.reachable_spots:
                spot.color = CROW_COLOR
                spot.is_empty = False
                flag = 1
                clear()
                spot.draw_circle()
            else:
                print("Click on a valid spot")
                flag = 0
    #check whether vulture have a valid move here
        
    if flag == 1: 
        if check_move(spot_list,vulture_prevloc.index) or check_capture(spot_list,vulture_prevloc.index):
            t.getscreen().onscreenclick(vulture_turn)
        else:
            print("Crow Win")
            crow_win_text = "Crows Win!!"
            t.penup()
            t.goto(0, window_height() / 2 - 60)
            t.pendown()
            t.color(CROW_COLOR)
            t.write(crow_win_text,align="center",font=("Arial", 46, "normal"))
            time.sleep(3)
            Screen().bye()
            return
    elif flag == 0:
        t.getscreen().onscreenclick(crow_turn2)


def vulture_turn(x, y):
    global vulture_prevloc
    global no_crows
    global no_crows_captured
    flag = -1
    flag1 = 1
    for spot in spot_list:
        distance = ((x - spot.x) ** 2 + (y - spot.y) ** 2) ** 0.5
        if distance <= spot.radius:
            if spot.is_empty and (spot.index in vulture_prevloc.reachable_spots or spot.index in vulture_prevloc.capturable_spots):
                if spot.index in vulture_prevloc.capturable_spots:
                    flag1 = 0
                    for crow in spot_list:
                        if crow.color == CROW_COLOR:
                            if (int(spot.y - crow.y) > 0 and int(crow.y - vulture_prevloc.y) > 0) or (int(spot.y - crow.y) < 0 and int(crow.y - vulture_prevloc.y) < 0):
                                if (int(spot.x - crow.x) > 0 and int(crow.x - vulture_prevloc.x) > 0) or (int(spot.x - crow.x) < 0 and int(crow.x - vulture_prevloc.x) < 0):
                                    # print(spot.y,crow.y,vulture_prevloc.y)
                                    no_crows_captured += 1
                                    crow.color = "white"
                                    crow.is_empty = True
                                    flag1 = 1
                                    # print("Hello")
                                    crow.draw_circle()
                            else:
                                if ((vulture_prevloc.index == 2 and crow.index == 3 ) or (vulture_prevloc.index == 3 and crow.index == 4) or (vulture_prevloc.index == 4 and crow.index == 3) or (vulture_prevloc.index == 5 and crow.index == 4)) and spot.index <= 5:
                                    crow.color = "white"
                                    no_crows_captured += 1
                                    crow.is_empty = True
                                    flag1 = 1
                                    # print("Hi")
                                    crow.draw_circle()
                    # print(f"Number Of Crows Captured:{no_crows_captured}")
                    if no_crows_captured == TARGET_CROWS:
                        print("Vulture wins")
                        vulture_win_text = "Vulture Win!!"
                        t.penup()
                        t.goto(0, window_height() / 2 - 60)
                        t.pendown()
                        t.color(VULTURE_COLOR)
                        t.write(vulture_win_text,align="center",font=("Arial", 46, "normal"))
                        time.sleep(3)
                        Screen().bye()
                        return
                if flag1 == 1:
                    if no_crows > 1:
                        vulture_prevloc.color = "white"
                        vulture_prevloc.is_empty = True
                        clear()
                        vulture_prevloc.draw_circle()

                    spot.color = VULTURE_COLOR
                    spot.is_empty = False
                    flag = 1
                    vulture_prevloc = spot
                    clear()
                    spot.draw_circle()
                else:
                    print("Click a valid spot")
                    flag = 0
            else:
                print("Click a valid spot")
                flag = 0
    if flag == 1:
        t.getscreen().onscreenclick(crow_turn1) 
    elif flag == 0:
        t.getscreen().onscreenclick(vulture_turn)

draw_star()
# t.penup()
# t.goto(I5.x+50, I5.y)
# t.pendown()

spot_list = [I1,I2,I3,I4,I5,I6,I7,I8,I9,I10]
for spot in spot_list:
    # print(spot)
    draw_circle(spot,25,"white")


t.getscreen().onscreenclick(crow_turn1)

mainloop()
