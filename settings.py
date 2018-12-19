class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.bullet_color = 60, 60, 60

        self.bullet_width = 3
        self.bullet_height = 15

        self.bullets_allowed = 20
        self.fleet_drop_speed = 10

        self.ship_limit = 3
        # 以什麼樣的速度加快遊戲節奏
        self.speedup_scale = 1

        self.initialize_dynamic_settings()
        #记分
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.1

        # fleet_direction 为1表示向右，为-1 表示向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
