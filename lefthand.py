# import turtle                    # import turtle library
# import sys
from runner import runner
                

class lefthand(runner):
    def __init__(self,x,y,walls,finish):
        super().__init__(x,y,walls)
        self.walls = walls
        self.finish = finish
        self.name = 'Left-Hand Rule Algorithm'
        self.path_length = 0
           
    def go_down(self):
        if (self.heading() == 270):                   # check to see if the sprite is pointing down
            x_walls = round(self.xcor(),0)          # sprite x coordinates =
            y_walls = round(self.ycor(),0)
            if (x_walls, y_walls) in self.finish:          # if sprite and the
                print("Finished")
            if (x_walls +24, y_walls) in self.walls:          # check to see if they are walls on the left
                if(x_walls, y_walls -24) not in self.walls:   # check to see if path ahead is clear
                    self.forward(24)
                    self.stamp()
                    self.path_length += 1
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)
                self.stamp()
                self.path_length += 1


    def go_left(self):
        if (self.heading() == 0):
            x_walls = round(self.xcor(),0)
            y_walls = round(self.ycor(),0)
            if (x_walls, y_walls) in self.finish:   # check turtle coordinates are at the finish line
                print("Finished")
            if (x_walls, y_walls +24) in self.walls:       # check to see if they are walls on the left
                if(x_walls +24, y_walls) not in self.walls:
                    self.forward(24)
                    self.stamp()
                    self.path_length += 1
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)
                self.stamp()
                self.path_length += 1


    def go_up(self):
        if (self.heading() == 90):
            x_walls = round(self.xcor(),0)
            y_walls = round(self.ycor(),0)
            if (x_walls, y_walls) in self.finish:   # check turtle coordinates are at the finish line
                print("Finished")
            if (x_walls -24, y_walls ) in self.walls:  # check to see if they are walls on the left
                if (x_walls, y_walls + 24) not in self.walls:
                    self.forward(24)
                    self.stamp()
                    self.path_length += 1
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)
                self.stamp()
                self.path_length += 1

    def go_right(self):
        if (self.heading() == 180):
            x_walls = round(self.xcor(),0)
            y_walls = round(self.ycor(),0)
            if (x_walls, y_walls) in self.finish:   # check turtle coordinates are at the finish line
                print("Finished")
            if (x_walls, y_walls -24) in self.walls:  # check to see if they are walls on the left
                if (x_walls - 24, y_walls) not in self.walls:
                    self.forward(24)
                    self.stamp()
                    self.path_length += 1
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)
                self.stamp()
                self.path_length += 1
    
    def completed(self):
        x_walls = round(self.xcor(),0)
        y_walls = round(self.ycor(),0)
        state = False
        if (x_walls, y_walls) in self.finish:   # check turtle coordinates are at the finish line
            print("Finished")
            state = True
        return state
    
