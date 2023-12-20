import util


class PlayerStatus:
    action = 0  # 0 - Walk / 1 - Run
    frame = 0
    player_position = [0, 0]  # X, Y
    old_direction = False  # False - Right / True - Left
    left = False
    right = False
    speed_x = 0.00
    speed_y = 0.00
    walk_acceleration = 0.00
    walk_slowdown = 0.00
    max_speed_x = 0.00
    max_speed_y = 0.00

    sword_equipped = True
    
    def __init__(self, walk_acceleration, walk_slowdown, max_speed_x, max_speed_y):
        self.walk_acceleration = walk_acceleration
        self.walk_slowdown = walk_slowdown
        self.max_speed_x = max_speed_x
        self.max_speed_y = max_speed_y
        
    def speedControl(self):
        if self.right and self.left:
            if abs(self.speed_x) <= self.walk_slowdown:
                self.speed_x = 0.00
            else:
                self.speed_x += -1 * util.sign(self.speed_x) * self.walk_slowdown
        elif self.right:
            self.speed_x += self.walk_acceleration

            if self.speed_x > self.max_speed_x:
                self.speed_x = self.max_speed_x

        elif self.left:
            self.speed_x -= self.walk_acceleration

            if abs(self.speed_x) > self.max_speed_x:
                self.speed_x = -1 * self.max_speed_x

        else:
            if abs(self.speed_x) <= self.walk_slowdown:
                self.speed_x = 0.00
            else:
                self.speed_x += -1 * util.sign(self.speed_x) * self.walk_slowdown

    def actionControl(self):
        if self.speed_x != 0.00:
            if self.sword_equipped and self.action != 3:
                self.action = 3
                self.frame = 0
            elif not self.sword_equipped and self.action != 1:
                self.action = 1
                self.frame = 0

        elif self.speed_x == 0.00:
            if self.sword_equipped and self.action != 2:
                self.action = 2
                self.frame = 0
            elif not self.sword_equipped and self.action != 0:
                self.action = 0
                self.frame = 0

    def positionControl(self):
        if 0 < self.speed_x < 5:
            self.player_position[0] += 0.1
        elif self.speed_x >= 5:
            self.player_position[0] += 0.2

        if -5 < self.speed_x < 0:
            self.player_position[0] -= 0.1
        elif self.speed_x <= -5:
            self.player_position[0] -= 0.2
