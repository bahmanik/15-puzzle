#memory leak in self.draw_tiles()
import pygame
import random
import time
from sprite import *
from setting import *
#from AI import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.button_list = []
        self.button_list.append(button(775, 100, 200, 50, "shuffle", White, Black))
        self.button_list.append(button(775, 170, 200, 50, "reset", White, Black))
        self.shuffle_start = False
        self.privios_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_complete = self.create_game()
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        
        self.draw_tiles()
        
    def shuffle(self):
        possible_moves = []
        for row, Tile in enumerate(self.tiles):
            for col, Tile in enumerate(Tile):
                if Tile.text == "empty":
                    if Tile.right():
                        possible_moves.append("right")
                    if Tile.left():
                        possible_moves.append("left")
                    if Tile.up():
                        possible_moves.append("up")
                    if Tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break
        choice = random.choice(possible_moves)
        
        if self.privios_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
            
        elif self.privios_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
            
        elif self.privios_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
            
        elif self.privios_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        self.privios_choice = choice
        
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col+1] = self.tiles_grid[row][col+1], self.tiles_grid[row][col]
            
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col-1] = self.tiles_grid[row][col-1], self.tiles_grid[row][col]
            
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row-1][col] = self.tiles_grid[row-1][col], self.tiles_grid[row][col]
            
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row+1][col] = self.tiles_grid[row+1][col], self.tiles_grid[row][col]
        
    def create_game(self):
        grid = [[x + y * GAMESIZE for x in range(1, GAMESIZE+1)]for y in range(GAMESIZE)]
        grid[-1][-1] = 0
        return grid
        
    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, Tile in enumerate(x):
                if Tile != 0:
                    self.tiles[row].append(tile(self, col, row, str(Tile)))
                elif Tile == 0:
                    self.tiles[row].append(tile(self, col, row, "empty"))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def pouse(self):
        pass
    
    def drawGrid(self):
        for row in range(-1, GAMESIZE*TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAMESIZE*TILESIZE))
        for col in range(-1, GAMESIZE*TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAMESIZE*TILESIZE, col))
    
    def draw(self):
        self.screen.fill(BGcolor)
        self.all_sprites.draw(self.screen)
        self.drawGrid()
        for buttons in self.button_list:
            buttons.draw(self.screen)
        UIelement(825, 35, "%.3f" % self.elapsed_time).draw(self.screen)

        pygame.display.flip()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, Tile in enumerate(self.tiles):
                    for col, Tile in enumerate(Tile):
                        if Tile.click(mouse_x, mouse_y):
                            if Tile.right() and self.tiles_grid[row][col+1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col+1] = self.tiles_grid[row][col+1], self.tiles_grid[row][col]
                            
                            if Tile.left() and self.tiles_grid[row][col-1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col-1] = self.tiles_grid[row][col-1], self.tiles_grid[row][col]
                                
                            if Tile.up() and self.tiles_grid[row-1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row-1][col] = self.tiles_grid[row-1][col], self.tiles_grid[row][col]
                                
                            if Tile.down() and self.tiles_grid[row+1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row+1][col] = self.tiles_grid[row+1][col], self.tiles_grid[row][col]
                                
                            self.draw_tiles()
                            
                for buttons in self.button_list:
                    if buttons.click(mouse_x, mouse_y):
                        if buttons.text == "reset":
                            self.new()
                        if buttons.text == "shuffle":
                            self.shuffle_time = 0
                            self.shuffle_start = True

    
    def update(self):
        self.all_sprites.update()
        
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_complete:
                self.start_game = False
                
            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer
                
        if self.shuffle_start:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time == 90:
                self.shuffle_start = False
                self.start_game = True
                self.start_timer = True
                print(self.tiles_grid)

    
game = Game()
    
while True:
    game.new()
    game.run()