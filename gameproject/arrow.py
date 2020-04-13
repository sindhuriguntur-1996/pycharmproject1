import pygame
from pygame.sprite import Sprite

class Arrow(Sprite):

    def __init__(self,ai_settings,screen):
        super(Arrow,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/bow-and-arrow.bmp')
        #self.image = pygame.transform.scale(image, (1280, 720))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center=float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_settings.arrow_speed
        elif self.moving_left and self.rect.left>self.screen_rect.left:
            self.center-=self.ai_settings.arrow_speed
        self.rect.centerx=self.center

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def center_arrow(self):
        self.center = self.screen_rect.centerx