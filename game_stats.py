# coding=utf-8
class Gamestats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 让游戏一开始出于非活动状态
        self.game_active = False

    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
