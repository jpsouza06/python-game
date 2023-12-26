import util


class PlayerStatus:
    action = 0  # 0 - Walk / 1 - Run
    frame = 0
    player_position = [0, 0]  # X, Y

    old_direction = False  # False - Right / True - Left
    left = False
    right = False
    down = False
    jumping = False
    jump = False
    ground = False

    collided_right = False
    collided_left = False
    collided_up = False
    collided_down = False

    speed_x = 0.00
    speed_y = 0.00
    walk_acceleration = 0.00
    walk_slowdown = 0.00
    max_speed_x = 0.00
    max_speed_y = 0.00
    max_speed_down = 0.00
    gravity = 5

    sword_equipped = True
    
    def __init__(self, walk_acceleration, walk_slowdown, max_speed_x, max_speed_y, player_postion, gravity, max_speed_down):
        self.walk_acceleration = walk_acceleration
        self.walk_slowdown = walk_slowdown
        self.max_speed_x = max_speed_x
        self.max_speed_y = max_speed_y
        self.player_position = player_postion
        self.gravity = gravity
        self.max_speed_down = max_speed_down

    def speedYControl(self):
        if self.jump and self.ground:
            self.jump = False
            self.ground = False
            self.speed_y = self.max_speed_y

        if not self.ground:
            self.speed_y -= self.gravity

        if abs(self.speed_y) > self.max_speed_y:
            self.speed_y = self.max_speed_y * util.sign(self.speed_y)

        if self.collided_up and self.speed_y > 0:
            self.speed_y = 0

        if self.collided_down and self.speed_y < 0:
            self.speed_y = 0

    def speedXControl(self):
        if self.right and self.left:
            if abs(self.speed_x) <= self.walk_slowdown:
                self.speed_x = 0.00
            else:
                self.speed_x += -1 * util.sign(self.speed_x) * self.walk_slowdown

        elif self.right:
            self.speed_x += self.walk_acceleration

            if self.down and self.speed_x > self.max_speed_down:
                self.speed_x = self.max_speed_down
            elif self.speed_x > self.max_speed_x:
                self.speed_x = self.max_speed_x

        elif self.left:
            self.speed_x -= self.walk_acceleration

            if self.down and abs(self.speed_x) > self.max_speed_down:
                self.speed_x = -1 * self.max_speed_down
            elif abs(self.speed_x) > self.max_speed_x:
                self.speed_x = -1 * self.max_speed_x

        else:
            if abs(self.speed_x) <= self.walk_slowdown:
                self.speed_x = 0.00
            else:
                self.speed_x += -1 * util.sign(self.speed_x) * self.walk_slowdown

        if self.collided_right and self.speed_x > 0:
            self.speed_x = 0

        if self.collided_left and self.speed_x < 0:
            self.speed_x = 0

    def actionControl(self):
        print(self.speed_y, self.player_position[1])
        if self.collided_left and self.left:
            if self.sword_equipped and self.action != 3:
                self.action = 3
                self.frame = 0
            elif not self.sword_equipped and self.action != 1:
                self.action = 1
                self.frame = 0

        elif self.jumping and not self.ground:
            if self.sword_equipped and self.action != 7:
                self.action = 7
                self.frame = 0
            elif not self.sword_equipped and self.action != 6:
                self.action = 6
                self.frame = 0

        elif self.down and self.speed_x != 0.00:
            if self.action != 5:
                self.action = 5
                self.frame = 0

        elif self.down and self.speed_x == 0.00:
            if self.action != 4:
                self.action = 4
                self.frame = 0

        elif self.speed_x != 0.00:
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
        if self.speed_x > 0 and self.down:
            self.player_position[0] += abs(self.speed_x)
        elif self.speed_x > 0:
            self.player_position[0] += abs(self.speed_x)

        if self.speed_x < 0 and self.down:
            self.player_position[0] -= abs(self.speed_x)
        elif self.speed_x < 0:
            self.player_position[0] -= abs(self.speed_x)

        if self.speed_y > 0:
            self.player_position[1] -= abs(self.speed_y)
        elif self.speed_y < 0:
            self.player_position[1] += abs(self.speed_y)

        if self.collided_up:
            self.player_position[1] += 2
            self.collided_up = False

        if self.collided_down and not self.ground:
            self.player_position[1] -= 2
            self.collided_down = False

        if self.collided_left:
            self.player_position[0] += 2
            self.collided_left = False

        if self.collided_right:
            self.player_position[0] -= 2
            self.collided_right = False

