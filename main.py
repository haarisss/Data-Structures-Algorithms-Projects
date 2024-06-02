import turtle
import networkx as nx
from runner import runner
from lefthand import lefthand
from dijkstra import dijkstra
from os.path import exists, join
from os import makedirs
import random


# X > Building (drone can’t go here)
# . > Road ( drone can fly here)
# s > The start location of the drone
# e > The pizza delivery location

#Tile size
tile_size = 24

#Draw map
def draw_map(map_file,tile_size=tile_size,cursor_size=20):
    global r
    global start,walls,finish,map_height,map_width
    global g
    #Pen
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.shape('square')
    pen.shapesize( tile_size / cursor_size)
    pen.color('black')
    pen.penup()
    pen.speed('fastest')
    # Read map file into array
    map_file = './maps/' + map_file
    map, start, walls, finish, nodes, edges = [], [], [], [], [], []
    with open(map_file) as file:
        for line in file:
            map.append(line.strip())
    map_height, map_width = len(map),len(map[0])
    
    # Draw map from array
    global start_x,start_y,end_x,end_y
    for y in range(map_height):
        for x in range(map_width):
            tile = map[y][x]
            screen_x = (x-map_width) * tile_size
            screen_y = (map_width-y) * tile_size
            
            #Walls
            if tile == 'X':
                pen.fillcolor('grey')
                walls.append((screen_x,screen_y))
            
            #Paths
            elif tile == '.':
                pen.fillcolor('white')
                nodes.append((screen_x,screen_y))
                if (screen_x-tile_size,screen_y) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x-tile_size,screen_y)))
                if (screen_x+tile_size,screen_y) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x+tile_size,screen_y)))
                if (screen_x,screen_y-tile_size) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x,screen_y-tile_size)))
                if (screen_x,screen_y+tile_size) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x,screen_y+tile_size)))
            
            #End
            elif tile == 'e':
                pen.fillcolor('sky blue')
                end_x, end_y = screen_x,screen_y  
                finish.append((end_x,end_y))
                nodes.append((screen_x,screen_y))
                if (screen_x-tile_size,screen_y) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x-tile_size,screen_y)))
                if (screen_x+tile_size,screen_y) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x+tile_size,screen_y)))
                if (screen_x,screen_y-tile_size) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x,screen_y-tile_size)))
                if (screen_x,screen_y+tile_size) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x,screen_y+tile_size)))
            
            #Start
            elif tile == 's':
                pen.fillcolor('spring green')
                start_x = (x-map_width) * tile_size
                start_y = (map_width-y) * tile_size
                start.append((start_x,start_y))
                nodes.append((screen_x,screen_y))
                if (screen_x-tile_size,screen_y) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x-tile_size,screen_y)))
                if (screen_x+tile_size,screen_y) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x+tile_size,screen_y)))
                if (screen_x,screen_y-tile_size) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x,screen_y-tile_size)))
                if (screen_x,screen_y+tile_size) in nodes:
                    edges.append(((screen_x,screen_y),(screen_x,screen_y+tile_size)))

            #Create tile
            pen.goto(screen_x,screen_y)
            pen.stamp()

    #Graph of path coords
    g = nx.Graph()
    g.add_edges_from(edges)

#Display user key controls
def controls(spacing= tile_size * 2):
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.up()
    pen.speed('fastest')
    pen.setheading(270)
    x, y = map_width+spacing, (map_height+3.5) * tile_size
    pen.goto(x,y)
    controls = [
        'Tab - Switch Algorithm',
        'R - Restart',
        'E - Change Map',
        'Click on a tile to set it as the goal',
        'S - Save Map',
        'G - Generate map',
        'M - Move sprite',
        'D- Default',
        'Esc - Exit'
    ]
    #show key controls
    pen.write('CONTROLS',font=('Arial',18,'bold','underline'))
    for i in controls:
        pen.forward(tile_size)
        pen.write(f'{i}',font=('Arial',12,'normal'))

#Init turtle screen
screen = turtle.Screen()
screen.setup(700, 700)
pen = turtle.Turtle()
pen.hideturtle()

#Switch to LHR algorithm
def switch_a():
    r.clear()
    return algo_a()

#Switch to Dijkstra's algorithm
def switch_b():
    r.clear()
    return algo_b()


#Display Algorithm info
def info(r):
    global pen
    algo = r.name
    path_length = r.path_length
    pen.clear()
    pen.up()
    pen.color('black')
    pen.speed('fastest')
    pen.setheading(270)
    x, y = (-map_width-0.5) * tile_size, map_height
    pen.goto(x,y)
    #show info
    pen.write('INFO',font=('Arial',16,'bold','underline'))
    pen.forward(tile_size)
    pen.write('Algorithm: {0}'.format(algo),font=('Arial',12,'normal'))
    pen.forward(tile_size)
    pen.write('Path Length: {0} Tiles'.format(path_length),font=('Arial',12,'normal'))

#Display Name & Class 
def credits():
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.up()
    pen.speed('fastest')
    x, y = (-map_width-0.5) * tile_size, map_height+310
    pen.goto(x,y)
    pen.write('PIZZA RUNNERS: Done by Kaung Khant & Haaris Sulaiman, DAAA/FT/2B/01',font=('Arial',12,'bold'))

#Display error msg
def err(msg):
    global pen
    pen.clear()
    pen.up()
    pen.speed('fastest')
    x, y = (-map_width-0.5) * tile_size, map_height
    pen.goto(x,y)
    pen.write(msg,font=('Arial',12,'normal'))

# LEFT HAND
def algo_a():
    global screen, r
    r.clear()
    r = lefthand(start_x,start_y,walls,finish)
    while True:
        #Check if path exists
        try:
            nx.shortest_path(g,(start_x,start_y),(end_x,end_y))
        except nx.exception.NetworkXNoPath:
            return err('There is no available path.')
        #Move
        r.go_right()
        r.go_down()
        r.go_left()
        r.go_up()
        screen.title(f'Algorithm: {r.name}, Path Length: {r.path_length}')
        if r.completed():
            info(r)
            screen.onkey(algo_a, 'r')   #r to restart algorithm
            screen.onkey(switch_b, 'Tab') #Tab to switch algorithms
            screen.onkey(roaming, 'm')
            screen.listen()
            break

#DIJKSTRA
def algo_b():
    global screen, r
    r.clear()
    r = dijkstra(start_x,start_y,g,finish,walls)
    while True:
        #Move unless no available path
        try:
            r.move(screen)
        except nx.exception.NetworkXNoPath:
            return err('There is no available path.')
        if r.completed():
            info(r)
            screen.onkey(algo_b, 'r')   #r to restart algorithm
            screen.onkey(switch_a, 'Tab')   #Tab to switch algorithms
            screen.onkey(roaming, 'm')
            screen.listen()
            break

# ------------------------------------------------------------------------------------
# Kaung Khant's Additional Features

#Map file text prompt (Kaung Khant Add. Feature 1)
def changeMap():
    global map
    #Dialog box for file name
    map = screen.textinput("Input map file","File")
    print(map)
    if map != None:
        #Add .txt to end if not in input
        if not map.endswith('.txt'):
            map += '.txt'
        #Check if file exists
        if not exists(f'./maps/{map}'):
            print(f"File {map} does not exist")
            return err(f'File {map} does not exist.')
        else:
            screen.clear()
            main()

#Change end goal (Kaung Khant Add. Feature 2)
def changeEnd(x,y,tile_size=tile_size,cursor_size=20):
    global finish
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.shape('square')
    pen.shapesize( tile_size / cursor_size)
    pen.color('black')
    pen.penup()
    pen.speed('fastest')
    #Check all paths
    for path in g.nodes():
        #Check if clicked coordinates in path tile
        if (x > (path[0]-tile_size*0.5) and x < (path[0]+tile_size*0.5)) and (y > (path[1]-tile_size*0.5) and y < (path[1]+tile_size*0.5)):
            #Go to end
            pen.goto(finish[0][0],finish[0][1])
            #Stamp as path
            pen.fillcolor('white')
            pen.stamp()
            #Replace finish coords with clicked tile
            finish = [(path[0],path[1])]
            #Go to new end
            pen.goto(finish[0][0],finish[0][1])
            #Stamp as end
            pen.fillcolor('sky blue')
            pen.stamp()
            break

#Save currently shown map as txt file
def save():
    #Dialog box for file name
    name = screen.textinput("Save Map","File Name")
    if name != None:
        #Create maps folder if it does not exist
        if not exists("maps"):
            makedirs("maps")
        #Add .txt to end if not in input
        if not name.endswith('.txt'):
            name += '.txt'
        #Map folder
        directory = './maps/'
        path = directory + name
        #Check if file already exists
        if exists(path):
            return err(f'File of name {name} already exists.')
        f = open(path, 'w')
        for y in range(map_height):
            row = ''
            for x in range(map_width):
                screen_x = (x-map_width) * tile_size
                screen_y = (map_width-y) * tile_size
                tile = (screen_x,screen_y)
                if tile in walls:
                    row += 'X'
                elif tile in finish:
                    row += 'e'
                elif tile in start:
                    row += 's'
                else:
                    row += '.'
            f.write(row + '\n')
        f.close()

# ------------------------------------------------------------------------------------
# HAARIS ADDITIONAL FEATURES


def roaming(): 
    global screen, r
    r.clear()
    r = runner(start_x,start_y,walls)
    r.goto(start_x,start_y)
    r.setheading(90)
    r.stamp()
    screen.title(f'Free Roaming Mode')
    # if (r.xcor(),r.ycor()+tile_size) in g.nodes:
    screen.onkeypress(r.sprite_up, "Up")
    # screen.onkeypress(r.go_up, "Up")
    # if (r.xcor(),r.ycor()-tile_size) in g.nodes:
    screen.onkeypress(r.sprite_down, "Down")
    # screen.onkeypress(r.go_down, "Down")
    # if (r.xcor()+tile_size,r.ycor()) in g.nodes:
    screen.onkeypress(r.sprite_right, "Right")
    # screen.onkeypress(r.go_right, "Right")
    # if (r.xcor()-tile_size,r.ycor()) in g.nodes:
    screen.onkeypress(r.sprite_left, "Left") 
    # screen.onkeypress(r.go_left, "Left")    
    screen.onkey(roaming, 'r')   #r to restart algorithm
    screen.onkey(default,'d')
    screen.onkey(switch_a, 'Tab')   #Tab to switch algorithms
    screen.listen()


# put start and end near walls

def generate_maze(width, height):
    global w, h, maze
    w , h = width , height
    maze = []
    for i in range(height):
        maze.append([])
        for j in range(width):
            if i == 0 or i == height-1 or j == 0 or j == width-1:
                maze[i].append("X")
            else:
                if (i > height//2 - 2 and i < height//2 + 2) and (j > width//2 - 2 and j < width//2 + 2):
                    if random.random() < 0.4: # chance of adding a wall is 40% in the center
                        maze[i].append("X")
                    else:
                        maze[i].append(".")
                else:
                    if random.random() < 0.2: # chance of adding a wall is 20% outside the center
                        maze[i].append("X")
                    else:
                        maze[i].append(".")

    start_x, start_y = random.randint(1, height-2), random.randint(1, width-2)
    end_x, end_y = random.randint(1, height-2), random.randint(1, width-2)

    while (start_x <= height//2 - 2 or start_x >= height//2 + 2) and (start_y <= width//2 - 2 or start_y >= width//2 + 2):
        start_x, start_y = random.randint(1, height-2), random.randint(1, width-2)

    while (end_x <= height//2 - 2 or end_x >= height//2 + 2) and (end_y <= width//2 - 2 or end_y >= width//2 + 2):
        end_x, end_y = random.randint(1, height-2), random.randint(1, width-2)

    maze[start_x][start_y] = "s"
    maze[end_x][end_y] = "e"

    return maze


def save_maze(maze):   
    global filename
    counter = 1
    if not exists("maps"):
        makedirs("maps")
    while True:
        filename = "extra_map_" + str(counter) + ".txt"
        file_path = join("maps", filename)
        if not exists(file_path):
            break
        counter += 1
    with open(file_path, "w") as f:
        for row in maze:
            f.write(''.join(row) + "\n")


def generate():
    global r
    screen.clear()
    maze = generate_maze(12, 8)
    save_maze(maze)
    print(filename)
    draw_map(filename)
    credits()
    controls()
    r = runner(start_x,start_y,walls)
    r.hideturtle()
    screen.onkey(screen.bye, "Escape")  #Esc to close screen
    screen.onkey(default,'d')
    screen.onkey(changeMap, 'e')   #e to choose map file
    screen.onkey(generate,'g')
    screen.onscreenclick(changeEnd) #Click on path tile to change it to the end tile
    screen.listen()
    algo_b()
    screen.mainloop()

def default():
    screen.clear()
    main()

# -------------------------------------------------------------------------

#Default Map
map = 'map01.txt'

#Main
def main():
    global r
    draw_map(map)   #Draw Map
    credits()   #Show Names and Class on topd
    controls()  #Show user controls
    r = runner(start_x,start_y,walls) #Initialize Runner
    screen.onkey(screen.bye, "Escape")  #Esc to close screen
    screen.onkey(changeMap, 'e')   #e to choose map file
    screen.onkey(save, 's') #s to save map
    screen.onkey(generate, 'g')
    screen.onscreenclick(changeEnd) #Click on path tile to change it to the end tile
    screen.listen()
    algo_a()    #Default start with Left-Hand
    screen.mainloop()


#Start
main()
