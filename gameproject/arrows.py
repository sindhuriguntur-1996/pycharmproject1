import pygame
from pygame.sprite import Sprite

class Arrows(Sprite):
    def  __init__(self,ai_settings,screen,arrow):
        super(Arrows,self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,ai_settings.arrows_width,ai_settings.arrows_height)
        self.rect.centerx = arrow.rect.centerx
        self.rect.top = arrow.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.arrows_color
        self.speed = ai_settings.arrows_speed

    def update(self):
        self.y-=self.speed
        self.rect.y=self.y

    def draw_arrows(self):
        pygame.draw.rect(self.screen,self.color,self.rect)