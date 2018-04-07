import pygame
# import numpy as np
import pyquil.api as api
from pyquil.gates import *
from pyquil.quil import Program

# open a QVM connection
qvm = api.QVMConnection()

# define colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red_blue = (255, 0, 255)
red_green = (255, 255, 0)
blue_green = (0, 255, 255)
color_code = 0
dartboard_A_color = (127.5, 127.5, 127.5)
# boolean controling when game stops
game_over = False
color_rect = True
# frames per second
fps = 60
# screen dimensions
size_x = 1000
size_y = 625
size = (size_x, size_y)
# dartboard parameters
radius_outer = 100
radius_1st_inner = 60
radius_2nd_inner = 20
width = 20

p = Program(H(0)).measure(0, [0])
results_A = qvm.run(p, [0])

results_B = []

# initialize pygame
pygame.init()
# setup screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Quantum darts")
# setup game clock
clock = pygame.time.Clock()
# define font
font = pygame.font.SysFont('Calibri', 25, True)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                color_code += 1
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass

    # set game color
    if color_code % 3 == 0:
        # make scren blue
        screen.fill(blue)
        # empty out results from dartboard_B
        if len(results_B) > 0:
            results_B.pop()
        text_results = font.render("results_A: " + str(results_A), True, (0, 0, 0))
        screen.blit(text_results, [500, 500])
        # set darboard_A centers, and calculate results_B in either case
        if results_A == [[0]]:
            dartboard_A_center = [size_x//2, size_y//2 - 150]
            p = Program(I(0), H(0)).measure(0, [0])
            results_B = qvm.run(p, [0])
        elif results_A == [[1]]:
            dartboard_A_center = [size_x//2, size_y//2 + 150]
            p = Program(X(0), H(0)).measure(0, [0])
            results_B = qvm.run(p, [0])
        print ("Results A: ", results_A)

    elif color_code % 3 == 1:
        screen.fill(red)
        if len(results_A) > 0:
            results_A.pop()
        text_results = font.render("results_B: " + str(results_B), True, (0, 0, 0))
        screen.blit(text_results, [500, 500])
        # set dartboard_B centers
        if results_B == [[0]]:
            dartboard_B_center = [size_x//2 + 150, size_y//2]
            p = Program(I(0), H(0)).measure(0, [0])
            results_A = qvm.run(p, [0])
        elif results_B == [[1]]:
            dartboard_B_center = [size_x//2 - 150, size_y//2]
            p = Program(X(0), H(0)).measure(0, [0])
            results_A = qvm.run(p, [0])
        print ("Results_B: ", results_B)

    elif color_code % 3 == 2:
        screen.fill(blue)

    pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    text_mouse = font.render("mouse buttons: " + str(pressed), True, (0, 0, 0))
    screen.blit(text_mouse, [size_x//2, size_y//2])
    text_mouse_pos = font.render("mouse position: " + str(mouse_pos), True, (0, 0, 0))
    screen.blit(text_mouse_pos, [100, 100])

    # draw dartboard
    if color_code % 3 == 0:
        pygame.draw.circle(screen, dartboard_A_color, dartboard_A_center, radius_outer, width)
        pygame.draw.circle(screen, dartboard_A_color, dartboard_A_center, radius_1st_inner, width)
        pygame.draw.circle(screen, dartboard_A_color, dartboard_A_center, radius_2nd_inner, width)
    elif color_code % 3 == 1:
        pygame.draw.circle(screen, dartboard_A_color, dartboard_B_center, radius_outer, width)
        pygame.draw.circle(screen, dartboard_A_color, dartboard_B_center, radius_1st_inner, width)
        pygame.draw.circle(screen, dartboard_A_color, dartboard_B_center, radius_2nd_inner, width)
    elif color_code % 3 == 2:
        pygame.draw.circle(screen, dartboard_A_color, dartboard_A_center, radius_outer, 10)

    pygame.display.flip()

    clock.tick(fps)
