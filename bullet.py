# coding=utf-8
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """创建一个子弹的对象，然后移动到飞船的头部"""

    def __init__(self, ai_settings, screen, ship):
        # 下面是python2.7版本的super用法，继承Sprite这个父类的__init__方法，就可以使用这个方法的所有函数
        super().__init__()
        self.screen = screen

        # 在（0,0）创建一个表示子弹的矩形，在设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 储存用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹的小数值，更新坐标，往上移动
        self.y -= self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


