# coding=utf-8
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import Gamestats


def check_keydown_events(event, ship, ai_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    # 开火时候检测，如果子弹数量少于setting里面限制数量才能开火
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_aliens(aliens):
    """更新外星人群中所有外星人的位置"""
    aliens.update()


def check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, screen, ship, ai_settings, bullets)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_settings, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, screen, ship, ai_settings, bullets):
    """在玩家单机Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 创建一群新的外星人，并将飞船放到屏幕中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人，第一个True为删除子弹，第二个为删除外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points
        sb.prep_score()

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船啊"""
    # 将ships_left减1
    if stats.ships_left > 0:
        stats.ships_left -= 1
        print(stats.ships_left)

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_screen(ship, ai_settings, screen, aliens, bullets, stats, play_button, sb):
    # 根据settings的颜色参数重新绘制屏幕颜色，如果先绘制屏幕后再进行子弹绘制，会出现子弹被屏幕遮挡的问题
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 如果游戏出于非活动状态，就绘制play按钮
    if stats.game_active == False:
        play_button.draw_button()
    sb.show_score()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_alien_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其加入当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings, screen)

    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人达到边缘时候采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
