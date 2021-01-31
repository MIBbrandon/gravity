from math import pi
from random import randint, uniform
from typing import List

import pygame

from Objects.Planet import Planet
from Objects.sun import sun
from Utils.calculations import calculations


class SolarSystem:
    """
    Some notes on the numbers used: since we can't perfectly compute everything, we scale it all up or down according to
    what best suits us. For example, a distance of 1 is equivalent to 1 million km, and a mass of 1 is equivalent to
    1.989E30 kg (the mass of the sun). We will insert the real values, but these will be proportionally dampened for the
    calculations and visualizations to take place.
    """
    nextID = 1
    alreadyPressed = False
    astralObjects = []
    checkingCollisionsToggle = True
    shiftPressed = False
    FPS = 60
    gravitationalConstant = 6.67E-11
    calc = calculations()

    # We will take in the address of the dashboard. This is useful for knowing it's position at all times
    dashboard = None

    velocityIncrease = 1.5E5

    def __init__(self, screen):
        self.screen = screen
        self.sun = sun(screen, 1.9891E30)
        self.astralObjects.append(self.sun)
        mercury = Planet(self.screen, 'mercury', [100, 100], [0, 0], 5, 3.2852E23)
        venus = Planet(self.screen, 'venus', [100, 200], [0, 0], 5, 4.867E24)
        earth = Planet(self.screen, 'earth', [100, 300], [0, 0], 5, 5.972E24)
        mars = Planet(self.screen, 'mars', [100, 400], [0, 0], 5, 6.39E23)
        jupiter = Planet(self.screen, 'jupiter', [100, 500], [0, 0], 5, 1.898E27)
        saturn = Planet(self.screen, 'saturn', [100, 600], [0, 0], 5, 5.683E26)
        uranus = Planet(self.screen, 'uranus', [200, 100], [0, 0], 5, 8.681E26)
        neptune = Planet(self.screen, 'neptune', [200, 200], [0, 0], 5, 1.024E26)
        self.astralObjects.append(mercury)
        self.astralObjects.append(venus)
        self.astralObjects.append(earth)
        self.astralObjects.append(mars)
        self.astralObjects.append(jupiter)
        self.astralObjects.append(saturn)
        self.astralObjects.append(uranus)
        self.astralObjects.append(neptune)

    def exist(self):
        """
        Allows everything in the Solar System to just happen
        """
        # Update FPS
        self.updateObjectsFPS(self.FPS)

        # Update if the mouse has clicked before already
        self.updateAlreadyPressed()

        # Add a planet when mouse is pressed (For adding planets)
        self.addPlanet()

        # Check collisions
        # self.checkCollisions()

        # Make every object attract each other
        self.applyAttraction()

        for object in self.astralObjects:
            if(object.id != 0):
                object.stabilizeOrbit(self)
                object.realMove()
                # pygame.draw.line(object.screen, object.colour,
                #                  [object.position[0],
                #                   object.position[1]],
                #                  [(self.sun.position[0]),
                #                   (self.sun.position[1])])
                pygame.draw.circle(self.screen, object.colour,
                                   [round(self.sun.position[0]), round(self.sun.position[1])],
                                   int(self.calc.getMagnitude([object.getPosition()[0]-self.sun.getPosition()[0],
                                                               object.getPosition()[1]-self.sun.getPosition()[1]])), 1)

        # self.printAllPlanetPositions()

    def applyAttraction(self):
        """
        Executes the attract() method of every object in the Solar System
        """
        for thing in self.astralObjects:
            if(thing.id != 0):  # If it's not the sun
                thing.attract(self.astralObjects, self.velocityIncrease)
        self.sun.attract(self.astralObjects, self.velocityIncrease)

    def checkCollisions(self):
        """
        Checks all objects to see if they have collided with something else. If they have, they are removed from
        self.astralObjects[]
        """
        if(self.checkingCollisionsToggle):
            # We first append everything that has collided to an array so that we don't just eliminate one of the
            # two objects
            toBeRemoved = []
            for thing in self.astralObjects:
                if thing.checkCollision(self.astralObjects):
                    toBeRemoved.append(thing)
            for thing in toBeRemoved:
                self.astralObjects.remove(thing)
            # We won't check collision for the sun since we don't want it to be destroyed

    def toggleCollision(self):
        """
        Calling this function toggles between checking for collisions and not. It is meant to be used only
        by the bToggleCollision class.
        """
        if(self.checkingCollisionsToggle):
            self.checkingCollisionsToggle = False
        else:
            self.checkingCollisionsToggle = True

    def addPlanet(self):
        """
        Adds a planet at the mouse position when the left mouse button is pressed (and is in the valid area of effect)
        """
        if(pygame.mouse.get_pos()[1] < pygame.display.get_surface().get_size()[1]-self.dashboard.height):
            if (pygame.mouse.get_pressed()[0] and not self.alreadyPressed):
                self.alreadyPressed = True

                # This just determines a limit for the values that a planet's velocity vector will randomly be assigned
                vlim = 0.06
                velocity = [uniform(-vlim, vlim), uniform(-vlim, vlim)]

                # Planet(screen, position, velocity, radius, mass, colour=[255, 255, 255])
                newPlanetRadius = 15
                newPlanetMass = 5.972E24

                newPlanet = Planet(self.screen, "planet", [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]], velocity, newPlanetRadius, newPlanetMass, [randint(0, 255), randint(0, 255), randint(0, 255)])
                newPlanet.id = self.nextID
                print(newPlanet.id)

                # Default is stable orbit
                newPlanet.stabilizeOrbit(self)

                self.nextID += 1
                self.astralObjects.append(newPlanet)

    def setPlanetPosition(self, planetName, position: List[int]):
        """
        Set the position of each planet
        :param planetName: name of the planet to be relocated
        :param position: list of type int with the position which the planet should take
        """
        for object in self.astralObjects:
            if(object.id != 0 and object.name == planetName):
                object.setPosition(position[0], position[1])

    def printAllPlanetPositions(self):
        for object in self.astralObjects:
            if(object.id != 0):
                print()
                print("Planet: " + object.name)
                print(object.getPosition())

    def getGravitationalConstant(self):
        return self.gravitationalConstant

    def removeAllPlanets(self):
        self.astralObjects.clear()
        self.astralObjects.append(self.sun)
        self.nextID = 1  # Resetting the id counter

    def updateFPS(self, FPS: int):
        self.FPS = FPS

    def updateObjectsFPS(self, FPS: int):
        for object in self.astralObjects:
            object.updateFPS(FPS)

    def updateAlreadyPressed(self):
        """
        If the left click is no longer being pressed, alreadyPressed goes to false
        """
        if (not pygame.mouse.get_pressed()[0]):
            self.alreadyPressed = False

    def obtainPointerToDashboard(self, dashboardPointer):
        self.dashboard = dashboardPointer
