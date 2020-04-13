import sys
import pygame
from settings import Settings
from arrow import Arrow
from arrows import Arrows
from pygame.sprite import Group
import gamefunctions as gf
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard
import pygame.mixer

def run_game():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_height,ai_settings.screen_width))
    pygame.display.set_caption("ALIEN INVASION")
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    arrow = Arrow(ai_settings,screen)
    bg_color = (100,230,200)
    num_of_arrows = Group()
    num_of_balloons = Group()
    gf.create_fleet(ai_settings, screen, arrow, num_of_balloons)
    pygame.mixer.music.load('sounds/bgmmusic.wav')
    pygame.mixer.music.play(-1)

    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,arrow,num_of_arrows,num_of_balloons)
        if stats.game_active:
            arrow.update()
            num_of_arrows.update()
        gf.update_each_arrows(ai_settings, screen,stats,sb,play_button, arrow,num_of_balloons,num_of_arrows)
        gf.update_balloons(ai_settings,stats,sb,screen,arrow,num_of_balloons,num_of_arrows)
        gf.update_screen(ai_settings,screen,stats,sb,arrow,num_of_arrows,num_of_balloons,play_button)

run_game()