
from Snake_Solve_Itself import *
from os import environ

# membuat frame GUI
def game_screen(frame):
    frame.fill(SURFACE)

# membuat garis pemisah antar petak
def game_grid(surface):
    x = 0
    y = 0
    for r in range(ROWS):
        x = x + SQUARE_SIZE
        y = y + SQUARE_SIZE
        pygame.draw.line(surface, GRID, (x, 0), (x, HEIGHT))
        pygame.draw.line(surface, GRID, (0, y), (WIDTH, y))


def mainkan(): # fungsi builder game
    pygame.init()
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Ular Anti-Tabrak")
    game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    speed = pygame.time.Clock()
    ular = Ular(game_surface)

    while True:
        game_screen(game_surface) # ukuran screen konsisten
        game_grid(game_surface) # ukuran grid konsisten

        ular.update() # mengembalikan kondisi paling update dari ular

        speed.tick(FPS) #ular bergerak dengan kecepatan yg sudah diatur
        pygame.display.update()


if __name__ == '__main__': # main function.
    mainkan()
