class Settings():
    def __init__(self):
        #screen settings
        self.screen_width = 600
        self.screen_height = 1000
        self.screen_bgcolor = (245,245,245)
        #arrow settings
        #self.arrow_speed = 2
        #bullet settings
       # self.arrows_speed = 1.5
        self.arrows_width = 3
        self.arrows_height = 10
        self.arrows_color = 0,0,0
        self.allowed_arrows = 3
        #balloon fleet settings
        #self.balloon_speed=1
        self.fleet_drop_speed = 10
        #self.fleet_direction = 1
        self.bow_limit = 3
        self.speedup_scale =1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.arrow_speed = 2
        self.arrows_speed = 1.5
        self.balloon_speed = 1
        self.fleet_direction = 1
        self.balloon_points = 50

    def increase_speed(self):
        self.arrow_speed *= self.speedup_scale
        self.arrows_speed *= self.speedup_scale
        self.balloon_speed *= self.speedup_scale
        self.balloon_points = int(self.balloon_points*self.score_scale)
        print(self.balloon_points)
