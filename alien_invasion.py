import pygame

from settings import Settings

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from game_stats import Gamestats

from button import Button
from scoreboard import Scoreboard


# from alien import Alien


def run_game():
    # 初始化背景设置
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 屏幕标题
    pygame.display.set_caption("123")
    # 创建飞船
    ship = Ship(ai_settings, screen)
    # 创建子弹，创建一个外星人编组
    bullets = Group()
    aliens = Group()
    stats = Gamestats(ai_settings)
    # 创建外星人
    # alien = Alien(ai_settings, screen)
    # 创建外星人群组
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 创建储存游戏统计信息的实例，并创建记分牌
    stats = Gamestats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 开始游戏主循环
    while True:
        play_button = Button(ai_settings, screen, "play")
        gf.check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens)
        # 创建play按钮

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)
        gf.update_screen(ship, ai_settings, screen, aliens, bullets, stats, play_button, sb)


run_game()
