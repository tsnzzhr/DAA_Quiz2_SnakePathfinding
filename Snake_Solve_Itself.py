import pygame
from copy import deepcopy
from random import randrange

#Frame Declaration
WIDTH = 302  #frame width
HEIGHT = 302  #frame length
ROWS = 10 #total block in each rows or columns
SQUARE_SIZE = WIDTH // ROWS #block size = width divided by rows
GAP_SIZE = 2  #gap between block (gridlines)

#Color Declaration (RGB Color)
SURFACE  = (51, 102, 0)
GRID = (201, 198, 172)
SNAKE = (255, 204, 102)
HEAD = (255, 204, 102)
VIRTUAL_SNAKE = (255, 0, 0)

#Game Bounderies
FPS = 15  #speed
INITIAL_SNAKE_LENGTH = 3 #initialize snake length
WAIT_SECONDS_AFTER_WIN = 30  #breaktime
max_starvation = ROWS * ROWS * ROWS * 2  #Max lives w
SNAKE_MAX_LENGTH = ROWS * ROWS - INITIAL_SNAKE_LENGTH  #Max apple can be eaten


GRID_ARRAY = [[i, j] for i in range(ROWS) for j in range(ROWS)] # 2D array


#Helper functions
def get_neighbour(position):
    neighbour = [[position[0] + 1, position[1]],
                 [position[0] - 1, position[1]],
                 [position[0], position[1] + 1],
                 [position[0], position[1] - 1]] #4 neighbour
    in_grid_neighbour = []
    for pos in neighbour: #check each neighbour from head, if in adjacency list will be add on the list
        if pos in GRID_ARRAY:
            in_grid_neighbour.append(pos)
    return in_grid_neighbour


def distance(pos1, pos2): #count distance with formula: sqrt(abs(x2-x1) + abs(y2-y1))
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)


#List of neighbour position
ADJACENCY_DICT = {tuple(pos): get_neighbour(pos) for pos in GRID_ARRAY}

#Define snake body
class Square:
    def __init__(self, pos, frame, check_apple=False):
        self.pos = pos #position
        self.frame = frame #drawGUI.
        self.check_apple = check_apple #initialize apple = 0
        self.check_tail = False #intialize no crash with the tail
        self.dir = [-1, 0]  #[x, y] Direction

        if self.check_apple:
            self.dir = [0, 0]

    def draw(self):
        x = self.pos[0]
        y = self.pos[1] #[x, y] between blocks
        ss = SQUARE_SIZE
        gs = GAP_SIZE

        #Draw snake body
        if self.dir == [0, 1]: #frame, color, point coordinates in x
            if self.check_tail:
                pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss - gs, ss - 2*gs, ss))

        if self.dir == [1, 0]:
            if self.check_tail:
                pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, SNAKE, (x * ss - gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [0, -1]:
            if self.check_tail:
                pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss + gs, ss - 2*gs, ss))

        if self.dir == [-1, 0]:
            if self.check_tail:
                pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss + gs, ss, ss - 2*gs))

        if self.check_apple:
            pygame.draw.rect(self.frame, SNAKE, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))

    def move(self, direction):
        self.dir = direction #self.dir is array of x and y position that set the next path
        self.pos[0] += self.dir[0] #self.pos is array of x and y position that set the actual position
        self.pos[1] += self.dir[1]

    def collision(self): #if the square position < or > from row and > -1
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False


class SNAKE:
    def __init__(self, frame):
        self.frame = frame
        self.check_mati = False
        self.squares_start_pos = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.frame, check_apple=True)

        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(Square(pos, self.frame))

        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.check_tail = True

        self.path = []
        self.is_SNAKE_virtual = False
        self.total_moves = 0
        self.won_game = False

    def draw(self):    
        self.apple.draw()
        self.head.draw()
        for sqr in self.squares[1:]:
            if self.is_SNAKE_virtual:
                sqr.draw(VIRTUAL_SNAKE)
            else:
                sqr.draw()

    def set_direction(self, direction):
        if direction == 'left':
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def handling(self): #check press quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit the game
                pygame.quit()

    def move(self): #Snake movement function
        for j, sqr in enumerate(self.squares):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turns:
                turn = self.turns[p]
                sqr.move([turn[0], turn[1]])
                if j == len(self.squares) - 1:
                    self.turns.pop(p)
            else:
                sqr.move(sqr.dir)
        self.moves_without_eating += 1

    def add_block(self): #add the snake tail
        self.squares[-1].check_tail = False
        tail = self.squares[-1]  #initial snake tail position

        direction = tail.dir
        if direction == [1, 0]: #append -> add the body +1
            self.squares.append(Square([tail.pos[0] - 1, tail.pos[1]], self.frame))
        if direction == [-1, 0]:
            self.squares.append(Square([tail.pos[0] + 1, tail.pos[1]], self.frame))
        if direction == [0, 1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] - 1], self.frame))
        if direction == [0, -1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] + 1], self.frame))

        self.squares[-1].dir = direction
        self.squares[-1].check_tail = True  #The snake body finale length

    def reset(self): #Return to new game
        self.__init__(self.frame)

    def end_collision(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos: #check head and tail collision
                return True

    def generate_apple(self): #random apple
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.frame, check_apple=True) #draw apple pada frame
        if not self.check_collision(self.apple.pos):
            self.generate_apple()

    def eat_apple(self): #check head = apple, no collision with virtual snake and haven't won
        if self.head.pos == self.apple.pos and not self.is_SNAKE_virtual and not self.won_game:
            self.generate_apple() # membuat apple baru
            self.moves_without_eating = 0 
            self.score += 1
            return True

    def go_to(self, position):#direct head to apple
        if self.head.pos[0] - 1 == position[0]:
            self.set_direction('left')
        if self.head.pos[0] + 1 == position[0]:
            self.set_direction('right')
        if self.head.pos[1] - 1 == position[1]:
            self.set_direction('up')
        if self.head.pos[1] + 1 == position[1]:
            self.set_direction('down')

    def check_collision(self, position):
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False #if position > or < frame and equal to - value, unsave position
        for sqr in self.squares: # iterative checking -> if the block = coordinates, unsave position
            if sqr.pos == position:
                return False
        return True

    # Breadth First Search Algorithm
    def bfs(self, start, end): #shortest path from start to end
        q = [start]  # Queue
        visited = {tuple(pos): False for pos in GRID_ARRAY}

        visited[start] = True

        #search for parent node to explore other path
        prev = {tuple(pos): None for pos in GRID_ARRAY}

        while q:  #queue in path
            node = q.pop(0) #path decrease from the first round
            neighbour = ADJACENCY_DICT[node]
            for next_node in neighbour:
                if self.check_collision(next_node) and not visited[tuple(next_node)]:
                    q.append(tuple(next_node)) #always filled if there's new node after in save position and haven't visited
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list() #save the parent node
        p_node = end  #search the parent node in each child node from the end node.

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == start:
                path.append(end)
                return path #if found the parent node, return to list path parent
            path.insert(0, p_node)

        return []  #Path not found or run out

    def create_SNAKE_virtual(self): #create virtual snake
        v_snake = SNAKE(self.frame)
        for i in range(len(self.squares) - len(v_snake.squares)):
            v_snake.add_block()

        for i, sqr in enumerate(v_snake.squares):
            sqr.pos = deepcopy(self.squares[i].pos)
            sqr.dir = deepcopy(self.squares[i].dir)

        v_snake.dir = deepcopy(self.dir)
        v_snake.turns = deepcopy(self.turns) # deepcopy is duplicate same as the source (array)
        v_snake.apple.pos = deepcopy(self.apple.pos)
        v_snake.apple.check_apple = True
        v_snake.is_SNAKE_virtual = True

        return v_snake

    def get_path_to_tail(self): #get distance to tail
        tail_pos = deepcopy(self.squares[-1].pos)
        self.squares.pop(-1)
        path = self.bfs(tuple(self.head.pos), tuple(tail_pos))
        self.add_block()
        return path

    def get_available_neighbour(self, pos): #initialize snake movement is save
        valid_neighbour = []
        neighbour = get_neighbour(tuple(pos))
        for n in neighbour:
            if self.check_collision(n) and self.apple.pos != n:
                valid_neighbour.append(tuple(n))
        return valid_neighbour

    def longest_path_to_tail(self): #farthest to tail
        neighbour = self.get_available_neighbour(self.head.pos)
        path = []
        if neighbour:
            dis = -9999
            for n in neighbour:
                if distance(n, self.squares[-1].pos) > dis:
                    v_snake = self.create_SNAKE_virtual()
                    v_snake.go_to(n)
                    v_snake.move()
                    if v_snake.eat_apple():
                        v_snake.add_block()
                    if v_snake.get_path_to_tail():
                        path.append(n)
                        dis = distance(n, self.squares[-1].pos)
            if path:
                return [path[-1]]

    def any_safe_move(self): #check movement probability
        neighbour = self.get_available_neighbour(self.head.pos)
        path = []
        if neighbour:
            path.append(neighbour[randrange(len(neighbour))])
            v_snake = self.create_SNAKE_virtual()
            for move in path:
                v_snake.go_to(move)
                v_snake.move()
            if v_snake.get_path_to_tail():
                return path
            else:
                return self.get_path_to_tail()

    def set_path(self):
        # 1 appleleft adjacent to head
        if self.score == SNAKE_MAX_LENGTH - 1 and self.apple.pos in get_neighbour(self.head.pos):
            winning_path = [tuple(self.apple.pos)]
            print('SNAKE berhasil memakan seluruh apple!\n')
            return winning_path

        v_snake = self.create_SNAKE_virtual()

        #virtual snake check the movement probability
        path_1 = v_snake.bfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))

        #path that follow tail virtual snake after visited path_1
        path_2 = []

        if path_1: # path_1 found the probability from bfs
            for pos in path_1: # direct virtual snake to apple
                v_snake.go_to(pos)
                v_snake.move()

            v_snake.add_block()  # virtual snake increase
            path_2 = v_snake.get_path_to_tail()

        if path_2:  # path between virtual snake and snake tail
            return path_1  # fastest and shortest bfs to apple

        # if path not found, virtual snake with tail or BFS not found to SNAKE
            # 1- make sure the farthest path to tail is available
            # 2- if even use longest_path_to_tail() to follow tail, if odd gunakan any_safe_move()
            # 3- change follow tail if stuck in loop
        if self.longest_path_to_tail() and self.score % 2 == 0 and self.moves_without_eating < max_starvation / 2:
            return self.longest_path_to_tail()

        if self.any_safe_move():
            return self.any_safe_move()

        #path to tail
        if self.get_path_to_tail():
            return self.get_path_to_tail() #shorthest path to tail

        print('No More Moves. Tidak ada path.\n')

    def update(self): #update snake position
        self.handling()

        self.path = self.set_path()
        if self.path:
            self.go_to(self.path[0])

        self.draw()
        self.move()

        if self.score == ROWS * ROWS - INITIAL_SNAKE_LENGTH:  # if block run out and fully filled by the snake body
            self.won_game = True

            pygame.time.wait(1000 * WAIT_SECONDS_AFTER_WIN)
            return 1

        if self.moves_without_eating == max_starvation: # block boundaries to move without eat the apple
            self.check_mati = True
            print("SNAKE kelaparan..\n")
            self.reset()

        if self.eat_apple(): #snake increase after eat the apple
            self.add_block()
