import sys
import pygame
from arrows import Arrows
from balloon import Balloon
from time import sleep
import pygame.mixer

pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

def check_keydown_events(event,ai_settings,screen,arrow,num_of_arrows):
    if event.key == pygame.K_RIGHT:
        arrow.moving_right = True
    elif event.key == pygame.K_LEFT:
        arrow.moving_left = True
    elif event.key == pygame.K_SPACE:
        firing_arrows(ai_settings, num_of_arrows, screen, arrow)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ai_settings,screen,arrow,num_of_arrows):
    if event.key == pygame.K_RIGHT:
        arrow.moving_right = False
    elif event.key == pygame.K_LEFT:
        arrow.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,arrow,num_of_arrows,num_of_balloons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,arrow,num_of_arrows)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ai_settings,screen,arrow,num_of_arrows)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,arrow,num_of_arrows,num_of_balloons,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,arrow,num_of_arrows,num_of_balloons,mouse_x,mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_highscore()
        sb.prep_level()
        sb.prep_arrownumbers()
        num_of_balloons.empty()
        num_of_arrows.empty()

        create_fleet(ai_settings,screen,arrow,num_of_balloons)
        arrow.center_arrow()

def update_screen(ai_settings,screen,stats,sb,arrow,num_of_arrows,num_of_balloons,play_button):
    screen.fill(ai_settings.screen_bgcolor)
    for each_arrow in num_of_arrows:
        each_arrow.draw_arrows()
    arrow.blitme()
    #balloon.blitme()
    num_of_balloons.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_each_arrows(ai_settings, screen,stats,sb,play_button, arrow,num_of_balloons,num_of_arrows):
    for each_arrow in num_of_arrows.copy():
        if each_arrow.rect.bottom<=0:
            num_of_arrows.remove(each_arrow)

    check_bullet_balloon_collision(ai_settings, screen,stats, sb, arrow, num_of_balloons, num_of_arrows)


def firing_arrows(ai_settings,num_of_arrows,screen,arrow):
    if len(num_of_arrows) < ai_settings.allowed_arrows:
        new_arrow = Arrows(ai_settings, screen, arrow)
        num_of_arrows.add(new_arrow)
        #pygame.mixer.pause()
        #pygame.mixer.music.load('sounds/bulletsound.mp3')
        #pygame.mixer.music.play()
        #pygame.mixer.music.set_volume(0.9)
        # pygame.mixer.Channel(0).play()

        bullet = pygame.mixer.Sound('sounds/bulletsound1.ogg')
        bullet.play()


def get_num_of_balloons_x(ai_settings,balloon_width):
    availabale_space_x =  ai_settings.screen_width - balloon_width
    number_balloons_x =  int(availabale_space_x / (balloon_width))
    return number_balloons_x

def create_balloon(ai_settings,screen,num_of_balloons,balloon_number,row_number):
    balloon = Balloon(ai_settings, screen)
    balloon_width = balloon.rect.width
    balloon.x = balloon_width + 1.5*balloon_width * balloon_number  # spacing after balloons
    balloon.rect.x = balloon.x #spacing between balloons
    balloon.rect.y= balloon.rect.height +1.5* balloon.rect.height*row_number#spacing below balloons
    num_of_balloons.add(balloon)

def create_fleet(ai_settings,screen,arrow,num_of_balloons):
    balloon = Balloon(ai_settings, screen)
    number_balloons_x = get_num_of_balloons_x(ai_settings,balloon.rect.width)
    number_rows = get_number_of_rows(ai_settings, arrow.rect.height, balloon.rect.height)
    for row_number in range(number_rows):
        for balloon_number in range(number_balloons_x):
            create_balloon(ai_settings, screen, num_of_balloons,balloon_number,row_number)

def get_number_of_rows(ai_settings, arrow_height, balloon_height):
    available_space_y = (ai_settings.screen_height -(2* balloon_height) -(2* arrow_height))
    number_rows = int(available_space_y/(3*balloon_height))
    return number_rows

def update_balloons(ai_settings,stats,sb,screen,arrow,num_of_balloons,num_of_arrows):
    check_fleet_edges(ai_settings, num_of_balloons)
    num_of_balloons.update()
    if pygame.sprite.spritecollideany(arrow,num_of_balloons):
        ship_hit(ai_settings, stats, sb, screen, arrow, num_of_balloons, num_of_arrows)
        #print("ship hit!")
    check_aliens_bottom(ai_settings, stats, sb, screen, arrow, num_of_balloons, num_of_arrows)

def ship_hit(ai_settings,stats,sb,screen,arrow,num_of_balloons,num_of_arrows):
    if stats.bow_left > 0:
        stats.bow_left -= 1
        num_of_balloons.empty()
        num_of_arrows.empty()
        create_fleet(ai_settings, screen, arrow, num_of_balloons)
        arrow.center_arrow()
        sleep(0.5)
        sb.prep_arrownumbers()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_fleet_edges(ai_settings,num_of_balloons):
    for balloon in num_of_balloons.sprites():
        if balloon.check_edges():
            change_fleet_direction(ai_settings,num_of_balloons)
            break

def change_fleet_direction(ai_settings,num_of_balloons):
    for balloon in num_of_balloons.sprites():
        balloon.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_balloon_collision(ai_settings, screen,stats, sb, arrow, num_of_balloons, num_of_arrows):
    collisions = pygame.sprite.groupcollide(num_of_arrows, num_of_balloons, True, True)

    if len(num_of_balloons) == 0:
        num_of_arrows.empty()
        ai_settings.increase_speed()
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_settings,screen,arrow,num_of_balloons)

    if collisions:
        for num_of_balloons in collisions.values():
            stats.score  += ai_settings.balloon_points*len(num_of_balloons)
            sb.prep_score()
            #pygame.mixer.music.load('sounds/balloon.mp3')
            #pygame.mixer.music.play()
            balloon = pygame.mixer.Sound(file="sounds/balloon1.ogg")
            balloon.play()
        check_high_score(stats, sb)



def check_aliens_bottom(ai_settings,stats,sb,screen,arrow,num_of_balloons,num_of_arrows):
    screen_rect = screen.get_rect()
    for balloon in num_of_balloons.sprites():
        if balloon.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats,sb, screen, arrow, num_of_balloons, num_of_arrows)

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score = stats.score
        sb.prep_highscore()