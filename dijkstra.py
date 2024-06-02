from runner import runner
import networkx as nx


class dijkstra(runner):
    def __init__(self,start_x,start_y,graph,target,walls):
        super().__init__(start_x,start_y,walls)
        self.start_x = start_x
        self.start_y = start_y
        self.graph = graph
        self.name = "Dijkstra's Algorithm"
        self.path_length = 0
        self.target = target[0]
    

    '''Check if algorithm has reached the end goal'''
    def completed(self):
        x_walls = round(self.xcor(),0)
        y_walls = round(self.ycor(),0)
        state = False
        if (x_walls, y_walls) == self.target:   # check turtle coordinates are at the finish line
            print("Finished")
            state = True
        return state

    '''Generate shortest path'''
    def shortest_path(self):
        g = self.graph
        source = (self.start_x,self.start_y)
        path = nx.shortest_path(g,source,self.target)

        return path

    '''Move according the shortest path'''
    def move(self,screen):
        path = self.shortest_path()
        cur = (self.start_x,self.start_y)
        for step in path[1:]:
            if step[0] > cur[0]:
                self.go_right()
            elif step[0] < cur[0]:
                self.go_left()
            elif step[1] > cur[1]:
                self.go_up()
            elif step[1] < cur[1]:
                self.go_down()
            cur = step
            self.path_length += 1
            screen.title(f'Algorithm: {self.name}, Path Length: {self.path_length}')
