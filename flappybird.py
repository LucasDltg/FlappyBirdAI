import pygame
import Bird
import Pipe
import sys
import numpy
import NeuralNetwork as nn

def mexit(birds: list[Bird.Bird], weigth: list):
    for i in range(0, len(birds)):
        if birds[i].is_alive:
            print(weigth[i])
    sys.exit()

def startGame(weight, fps=60, graphic_enable=False):
    window_size = [600, 600]
    pipe_nb = 3
    bird_nb = len(weight)
    bird_startx = 50
    alpha = 150
    bird_color = [[255, 0, 0, alpha], [0, 255, 0, alpha], [0, 0, 255, alpha], [255, 255, 0, alpha], [255, 0, 255, alpha], [0, 255, 255, alpha], [255, 255, 255, alpha], [255, 127, 0, alpha], [255, 0, 127, alpha], [127, 255, 0, alpha], [0, 255, 127, alpha], [127, 0, 255, 0]]

    pipe_interspace = (280+window_size[0])/pipe_nb
    birds = [Bird.Bird(window_size, [bird_startx, window_size[1]/2], bird_color=bird_color[i%len(bird_color)]) for i in range(0, bird_nb)]
    pipes = [Pipe.Pipe(window_size, window_size[0]+i*pipe_interspace) for i in range(0, pipe_nb)]
    birds_alive = bird_nb
    scores = [float(0.0) for i in range(0, bird_nb)]

    if graphic_enable:
        black = (0, 0, 0)
        pygame.init()
        screen = pygame.display.set_mode(window_size)

    clock = pygame.time.Clock()
    while True:
        clock.tick(fps)
        if graphic_enable:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mexit(birds, weight)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mexit(birds, weight)
                    if event.key == pygame.K_SPACE:
                        for i in birds:
                            i.jump()

        #cherche le tuyau le plus proche en avant
        indmin = 0
        min_pipe = window_size[1]
        for i in range(0, pipe_nb):
            if pipes[i].pipe[0][0]+pipes[i].pipe_width > bird_startx and pipes[i].pipe[0][0] < min_pipe:
                min_pipe = pipes[i].pipe[0][0]
                indmin = i

        for i in range(0, bird_nb):
            #distance pipe-bird en x // distance bird au milieu tuyau en y (positif si bird au dessus de pipe)// vitesse
            #normalise
            if birds[i].is_alive:
                #calcul score
                birds[i].score = numpy.trunc(birds[i].score) + 0.9 - abs(((pipes[indmin].pipe[0][1] - pipes[indmin].pipe_interspace / 2) - birds[0].bird_pos[1])) / window_size[1]

                if nn.process((pipes[indmin].pipe[0][0]-birds[i].bird_pos[0])/window_size[0],
                          (pipes[indmin].pipe[0][1]-pipes[indmin].pipe_interspace/2-birds[i].bird_pos[1])/(window_size[1]/2),
                          birds[i].bird_yspeed/birds[i].bird_max_speed, weight[i]):
                    birds[i].jump()



        #update all the birds
        for i in range(0, bird_nb):
            if birds[i].is_alive:
                if birds[i].update() == -1:
                    birds[i].is_alive = False
                    birds_alive -= 1
                    scores[i] = birds[i].score

        # update all the pipes
        for i in range(0, pipe_nb):
            if pipes[i].update(pipes[(i-1)%pipe_nb].pipe[0][0]+pipe_interspace) == 1:
                for j in range(0, bird_nb):
                    if birds[j].is_alive:
                        birds[j].can_score = True
            #score if bird pass pipe
            for j in range(0, bird_nb):
                if birds[j].bird_pos[0] > pipes[i].pipe[0][0] + pipes[i].pipe[0][2]:
                    if birds[j].can_score and birds[j].is_alive:
                        birds[j].can_score = False
                        birds[j].score += 1

        #check les collisions
        for i in range(0, bird_nb):
            for j in pipes:
                if birds[i].is_alive:
                    if pygame.Rect(birds[i].bird_pos, birds[i].bird_size).colliderect(pygame.Rect(j.pipe[0])) or pygame.Rect(birds[i].bird_pos, birds[i].bird_size).colliderect(pygame.Rect(j.pipe[1])):
                        birds[i].is_alive = False
                        birds_alive -= 1
                        scores[i] = birds[i].score

        #si tout le monde est mort on quitte
        if birds_alive <= 0:
            return scores

        if graphic_enable:
            screen.fill(black)
            #draw all the birds in alpha mode
            for i in range(0, bird_nb):
                if birds[i].is_alive:
                    tsurf = pygame.Surface(birds[i].bird_size, pygame.SRCALPHA, 32)
                    tsurf = tsurf.convert_alpha()
                    tsurf.fill(birds[i].bird_color)
                    screen.blit(tsurf, birds[i].bird_pos)
            #draw all the pipes
            for i in range(0, pipe_nb):
                pygame.draw.rect(screen, pipes[i].pipe_color, pipes[i].pipe[0])
                pygame.draw.rect(screen, pipes[i].pipe_color, pipes[i].pipe[1])

            ind = 0
            #affichage score
            font = pygame.font.Font(pygame.font.get_default_font(), 32)
            for i in range(0, bird_nb):
                if birds[i].is_alive:
                    tscore = font.render(str(int(birds[i].score)), True, birds[i].bird_color)
                    tsize = tscore.get_size()
                    screen.blit(tscore, pygame.Rect((window_size[0]-tscore.get_size()[0],ind*tsize[1]), tsize))
                    ind+=1
            pygame.display.flip()


