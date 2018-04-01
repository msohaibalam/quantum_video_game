import pygame
import numpy as np
import pyquil.api as api
from pyquil.gates import *
from pyquil.quil import Program

# define colors
blue = (0, 0, 255)
circ_color = (127.5, 127.5, 255)
# boolean controling when game stops
game_over = False
# frames per second
fps = 60
# screen dimensions
size_x = 1000
size_y = 625
size = (size_x, size_y)

# create connection with quantum virtual machine
qvm = api.QVMConnection()
# create classical register
classical_reg = [0]
# initialize radius, and identify scale factor
radius = 50
scale_factor = 1.5
# initialize rotation angle
theta = 0
delta_theta = 0

# initialize pygame
pygame.init()

# setup screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Quantum video game mini-engine demo")
# setup game clock
clock = pygame.time.Clock()
# define font
font = pygame.font.SysFont('Calibri', 25, True)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    screen.fill(blue)

    #####################################################
    #### demo 1 -- circle expands/contracts randomly ####
    #####################################################
    p1 = Program()
    p1.inst(H(0))
    p1.measure(0, classical_reg[0])
    measure_qubit = [item for sublist in qvm.run(p1, classical_reg) for item in sublist]
    del p1

    if measure_qubit == [0]:
        radius = int(radius * scale_factor)
    elif measure_qubit == [1]:
        radius = int(radius/scale_factor)

    # this just makes sure circle doesn't become too small or big
    if radius < 20:
        radius = 20
    elif radius > 400:
        radius = 400

    pygame.draw.circle(screen, circ_color, [size_x//2, size_y//2], radius)

    #################################################################################################
    #### demo 2 -- wavefunction interpolates between |0> and |1> in response to UP/DOWN commands ####
    #################################################################################################
    pressed = pygame.key.get_pressed()
    # increase rotation angle if pressing UP
    if pressed[pygame.K_UP]:
        theta += np.pi/64.
    # decrease rotation angle if pressing DOWN
    if pressed[pygame.K_DOWN]:
        theta -= np.pi/64.

    # make sure theta stays between 0 and pi
    if theta < 0:
        theta = 0
    elif theta > np.pi:
        theta = np.pi

    p2 = Program()
    p2.inst(RY(theta)(0))
    wavefunc = qvm.wavefunction(p2)
    text_wavefunc = font.render("wavefunction: " + str(wavefunc), True, (0, 0, 0))
    text_theta = font.render("theta: " + str(theta), True, (0, 0, 0))
    screen.blit(text_wavefunc, [150, 20])
    screen.blit(text_theta, [150, 50])
    del p2

    pygame.display.flip()

    clock.tick(fps)
