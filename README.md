# DAA_Quiz2_SnakePathfinding

Group 23
Team :
1. Afifah Nur Sabrina Syamsudin (05111940000022)
2. Tsania Az Zahra (05111940000032)

## PROGRAM OVERVIEW :

this is an autonomous game that was made by implementing Breadth-First Search as its Solving-method the BFS function is written as below :
```
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
```

this program implies adjacency-paths that are definitely applying shortest path and fastest path that snake could reach the apple as the target. details could be shown in the source code attached above.

### HOW TO RUN THE PROGRAM
1. make sure that pygame has been installed properly. or simply just to call a command in terminal `pip install pygame`
2. run the `UtilityFunctions.py` program because the main functions of entire program exists inside, it is the main program.
3. graphical user interface of the game would appear immediately and the snake would run itself until it's done.

### PROBLEMS WHILE RUNNING PROGRAM
the program would be not responding after completing all path or has reached finish session. so it might take several times to wait and close the program using cross button on the corner of the interface.
