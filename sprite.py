from typing import Any
import pygame
from pygame.sprite import Group
from setting import *

pygame.font.init()

class tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50)
            font_surface = self.font.render(self.text, True, Black)
            self.image.fill(White)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE/2) - self.font_size[0] / 2
            draw_y = (TILESIZE/2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BGcolor)
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    def click(self, mouse_X, mouse_):
        return self.rect.left <= mouse_X <= self.rect.right and self.rect.top <= mouse_ <= self.rect.bottom
    
    def right(self):
        return self.rect.x + TILESIZE < GAMESIZE * TILESIZE
    
    def left(self):
        return self.rect.x - TILESIZE >= 0
    
    def up(self):
        return self.rect.y - TILESIZE >= 0
    
    def down(self):
        return self.rect.y + TILESIZE < GAMESIZE * TILESIZE
    
class UIelement:
    def __init__(self, x, y, text):
        self.text = text
        self.x ,self.y = x, y
        
    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 50)
        text = font.render(self.text, True, White)
        screen.blit(text, (self.x, self.y))
        
class button:
    def __init__(self, x, y, width, hieght,text, color, text_color):
        self.x, self.y = x, y
        self.width, self.hiegh = width, hieght
        self.color, self.text_color = color, text_color
        self.text = text
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.hiegh))
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_color)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width/2) - self.font_size[0] / 2
        draw_y = self.y + (self.hiegh/2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))
        
    def click(self, mouse_X, mouse_):
        return self.x <= mouse_X <= self.x + self.width  and self.y <= mouse_ <= self.y + self.hiegh