import pygame
from copy import deepcopy
from random import randrange

# Sizing
WIDTH = 302  # Lebar Frame
HEIGHT = 302  # Panjang Frame
ROWS = 10 # Banyak Kotak Dalam 1 Baris atau 1 Kolom
SQUARE_SIZE = WIDTH // ROWS # Besar Tiap Kotak = Width Dibagi Rows
GAP_SIZE = 2  # Gap Antara / Tebal Gridlines

# Warna-warna -> Pakai kode RGB
SURFACE  = (51, 102, 0)
GRID = (201, 198, 172)
ULAR = (255, 204, 102)
HEAD = (255, 204, 102)
VIRTUAL_ULAR = (255, 0, 0)

# Boundaries Pada Game
FPS = 15  # Kecepatan Ular
INITIAL_ULAR_LENGTH = 3 # Panjang Ular Pertama Kali
WAIT_SECONDS_AFTER_WIN = 30  # Transisi Memulai Dari Goal Menuju Reset Game
max_starvation = ROWS * ROWS * ROWS * 2  # Maksimal Banyak Petak Ular Tetap Hidup Tanpa Apel
ULAR_MAX_LENGTH = ROWS * ROWS - INITIAL_ULAR_LENGTH  # Maksimal Apel yang Dapat Dimakan Ular


GRID_ARRAY = [[i, j] for i in range(ROWS) for j in range(ROWS)] # array 2D sebesar 10x10


# Helper functions
def get_tetangga(position):
    tetangga = [[position[0] + 1, position[1]],
                 [position[0] - 1, position[1]],
                 [position[0], position[1] + 1],
                 [position[0], position[1] - 1]] # ada 4 tetangga
    in_grid_tetangga = []
    for pos in tetangga: # memeriksa tiap tetangga dari kepala ular jika ada pada adjacency list maka ditambahkan pada daftar
        if pos in GRID_ARRAY:
            in_grid_tetangga.append(pos)
    return in_grid_tetangga


def distance(pos1, pos2): # untuk menghitung jarak dengan rumus sqrt(abs(x2-x1) + abs(y2-y1))
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)


# List yang berisi koordinat tetangga
ADJACENCY_DICT = {tuple(pos): get_tetangga(pos) for pos in GRID_ARRAY}

# mendefinisikan setiap petak badan ular
class Square:
    def __init__(self, pos, frame, cek_apel=False):
        self.pos = pos # posisi
        self.frame = frame # screen GUI untuk diperlakukan drawGUI.
        self.cek_apel = cek_apel # asumsi tidak ada apel.
        self.cek_ekor = False # asumsi tidak menabrak ekor
        self.dir = [-1, 0]  # [x, y] Direction

        if self.cek_apel:
            self.dir = [0, 0]

    def draw(self):
        x = self.pos[0]
        y = self.pos[1] # x dan y jarak antar kotak
        ss = SQUARE_SIZE
        gs =  GAP_SIZE

        # menggambar objek badan berupa petak berwarna badan ular pada frame
        if self.dir == [0, 1]: # (frame, warna, koordinat titik-titik sudut pada persegi pada koordinat x)
            if self.cek_ekor:
                pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss - gs, ss - 2*gs, ss))

        if self.dir == [1, 0]:
            if self.cek_ekor:
                pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, ULAR, (x * ss - gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [0, -1]:
            if self.cek_ekor:
                pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss + gs, ss - 2*gs, ss))

        if self.dir == [-1, 0]:
            if self.cek_ekor:
                pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss + gs, ss, ss - 2*gs))

        if self.cek_apel:
            pygame.draw.rect(self.frame, ULAR, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))

    def move(self, direction):
        self.dir = direction # self.dir adalah array berisi posisi x dan y yang menyimpan tujuan jalan setelahnya
        self.pos[0] += self.dir[0] # self.pos adalah array yang berisi posisi x dan y yang menyimpan posisi saat ini
        self.pos[1] += self.dir[1]

    def menabrak(self): # jika posisi square kurang atau lebih dari row, dan kurang dari -1
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False
