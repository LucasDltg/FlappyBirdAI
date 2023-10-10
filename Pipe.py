import random


class Pipe:
    #stocke x y width height
    pipe = [[], []]
    pipe_width = 50
    pipe_interspace = 0
    pipe_speed = 3
    pipe_minimum_height = 50
    pipe_nb = 3
    pipe_color = [0, 255, 0]

    def __init__(self, game_window_size, pipe_x, pipe_width=50, pipe_interspace=180, pipe_speed=3, pipe_minimum_height=50, pipe_color=[0, 255, 0]):
        self.game_window_size = game_window_size
        self.pipe_width = pipe_width
        self.pipe_interspace = pipe_interspace
        self.pipe_speed = pipe_speed
        self.pipe_minimum_height = pipe_minimum_height
        self.pipe_color = pipe_color

        self.pipe = self.generate_pipe(pipe_x)

    def generate_pipe(self, pipe_x):
        rh = random.randint(self.pipe_minimum_height+self.pipe_interspace, self.game_window_size[1]-self.pipe_minimum_height)
        return [[pipe_x, rh, self.pipe_width, self.game_window_size[1] - rh], [pipe_x, 0, self.pipe_width, rh-self.pipe_interspace]]

    def update(self, pipe_x):
        score=0
        # pipe disappear
        if self.pipe[0][0] + self.pipe_width < 0:
            self.pipe = self.generate_pipe(pipe_x)
            score = 1
        #recule pipe
        self.pipe[0][0] -= self.pipe_speed
        self.pipe[1][0] -= self.pipe_speed
        return score

