# Runner class
from turtle import Turtle

class runner(Turtle):
    def __init__(self,x,y,walls):
        super().__init__()
        self.hideturtle()
        self.color('red')
        self.penup()
        self.speed('slow')
        self.setheading(90)
        self.goto(x,y)
        self.stamp()
        self.walls = walls

    def go_left(self,length=24):
            #go left
            self.setheading(180)  #Face West
            self.forward(length)
            self.stamp()

    def go_right(self,length=24):
            #go right
            self.setheading(0) #Face East
            self.forward(length)
            self.stamp()

    def go_up(self,length=24):
            #go up
            self.setheading(90)  #Face North
            self.forward(length)
            self.stamp()

    def go_down(self,length=24):
            #go down
            self.setheading(270)    #Face South
            self.forward(length)
            self.stamp()

    def sprite_right(self,length=24):
        self.setheading(0)
        x_walls = round(self.xcor(),0)
        y_walls = round(self.ycor(),0)
        if ((x_walls + length), y_walls ) not in self.walls:  # check to see if they are walls on the left
            self.forward(24)
            self.stamp()
    
    def sprite_down(self,length = 24):
        self.setheading(270)
        x_walls = round(self.xcor(),0)
        y_walls = round(self.ycor(),0)
        if (x_walls, (y_walls - length) ) not in self.walls:  # check to see if they are walls on the left
            self.forward(24)
            self.stamp()
            
    def sprite_up(self,length=24):
        self.setheading(90)
        x_walls = round(self.xcor(),0)
        y_walls = round(self.ycor(),0)
        print(x_walls,y_walls)
        print((x_walls, (y_walls + length) ) not in self.walls)
        if (x_walls, (y_walls + length) ) not in self.walls:  # check to see if they are walls on the left
            self.forward(24)
            self.stamp()

    def sprite_left(self,length=24):
        self.setheading(180)
        x_walls = round(self.xcor(),0)
        y_walls = round(self.ycor(),0)
        if ((x_walls - length), y_walls ) not in self.walls:  # check to see if they are walls on the left
            self.forward(24)
            self.stamp()
            
