from pathlib import Path
import pygame
import os
from Utils.calculations import calculations
from math import *
from typing import List

class sun:
    base_path = Path(os.path.dirname(__file__)).parent
    sun_sprite_path = os.path.join(base_path, 'sprites', 'sun.png')
    image_width = 40
    image_height = 40
    c = calculations()

    # The values of these values are just placeholders. The real values will be given by setPosition
    position = [0, 0]
    realPosition = [0, 0]

    def __init__(self, screen, mass):
        self.id = 0
        self.screen = screen
        self.position[0] = int(self.position[0])
        self.position[1] = int(self.position[1])
        self.mass = mass
        self.colour = [255, 218, 10]
        self.radius = 30
        self.image = pygame.image.load(self.sun_sprite_path)
        self.image_width, self.image_height = self.image.get_size()

    def attract(self, astralObjects, velocityIncrease):
        pass
        # for object in astralObjects:
        #     if object.id != self.id:
        #         gravityForce = self.c.getGravityForce(self, object)
        #         self.c.applyAcceleration(object, gravityForce)

    def stabilizeOrbit(self, solarSystem):
        pass

    def checkCollision(self, astralObjects):
        return False

    def realMove(self):
        pass

    def getRadius(self):
        return self.radius

    def getPosition(self):
        return self.position

    def getRealPosition(self):
        return self.realPosition

    def getMass(self):
        return self.mass

    def setPosition(self, newPosition: List[int]):
        self.position = newPosition
        self.realPosition = [self.position[0] * 7.5E8, self.position[1] * 7.5E8]

    def updateFPS(self, FPS: int):
        pass

    def draw(self):
        # pygame.draw.circle(self.screen, self.colour, [round(self.position[0]), round(self.position[1])], int(200))

        # pygame.draw.rect(self.screen, self.colour, [self.position[0], self.position[1], self.radius, self.radius])
        self.screen.blit(self.image, [self.position[0]-(self.image_width/2), self.position[1]-(self.image_height/2)])
        # pygame.draw.arc(self.screen, self.colour, [round(self.position[0]-200), round(self.position[1]-200), 400, 400],
        #                 0, 2*pi + 1)
