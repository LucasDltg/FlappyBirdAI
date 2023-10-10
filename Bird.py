
class Bird:
    bird_pos = [0, 0]
    bird_size = [0, 0]
    bird_yspeed = 0
    bird_color = [255, 0, 0]
    score: float = 0.0
    can_score = True
    bird_max_speed = 15
    is_alive = True

    def __init__(self, game_window_size, bird_pos=[0, 0], bird_yspeed=0, bird_size=[30, 30], bird_color=[255, 0, 0]):
        self.game_window_size = game_window_size
        self.bird_pos = bird_pos
        self.bird_yspeed = bird_yspeed
        self.bird_size = bird_size
        self.bird_color = bird_color

    def jump(self):
        self.bird_yspeed = -self.bird_max_speed

    def update(self):

        #chute
        if self.bird_yspeed < 5:
            self.bird_yspeed += 1

        # update position
        self.bird_pos[1] += self.bird_yspeed

        #bounds
        if self.bird_pos[1] - self.bird_yspeed < 0:
            self.bird_pos[1] = 1
            self.bird_yspeed = 0
        elif self.bird_pos[1] + self.bird_size[1] > self.game_window_size[1]:
            self.bird_pos[1] = self.game_window_size[1]
            return -1


