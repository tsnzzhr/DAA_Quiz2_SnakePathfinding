# DAA_Quiz2_SnakePathfinding

Team :
1. Afifah Nur Sabrina Syamsudin (05111940000022)
2. Tsania Az Zahra (05111940000032)

## PROGRAM OVERVIEW :

this is an autonomous game that was made by implementing Breadth-First Search as its Solving-method the BFS function is written as below :
```
# Breadth First Search Algorithm
    def bfs(self, start, end):  # Jarak terpendek dari start ke end
        q = [start]  # Queue
        dikunjungi = {tuple(pos): False for pos in GRID_ARRAY}

        dikunjungi[start] = True

        # mencari parent node agar membuka path yang dapat ditempuh selain yang sudah dikunjungi
        prev = {tuple(pos): None for pos in GRID_ARRAY}

        while q:  # Ketika queue terdapat path
            node = q.pop(0) # path akan selalu berkurang terurut dari urutan pertama
            tetangga = ADJACENCY_DICT[node]
            for next_node in tetangga:
                if self.cek_aman(next_node) and not dikunjungi[tuple(next_node)]:
                    q.append(tuple(next_node)) # tetapi akan selalu terisi selama terdapat node baru setelahnya yang aman dan belum dikunjungi sebelumnya
                    dikunjungi[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = end  # mencari parent node dari tiap child node dimulai dari end node.

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == start:
                path.append(end)
                return path # jika parent ditemukan maka akan mengembalikan list path parent
            path.insert(0, p_node)

        return []  # Path tidak ada atau habis
```

this program implies adjacency-paths that are definitely applying shortest path and fastest path that snake could reach the apple as the target. details could be shown in the source code attached above.


### PROBLEMS WHILE RUNNING PROGRAM
the program would be not responding after completing all path or has reached finish session. so it might take several times to wait and close the program using cross button on the corner of the interface.
