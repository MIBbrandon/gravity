import math
import time
from math import *
from typing import List

import pygame

from Objects import Planet

def constrain(var, lowerLimit, upperLimit):
    if var < lowerLimit:
        return lowerLimit
    elif var > upperLimit:
        return upperLimit
    else:
        return var

# TODO: Change all mathematical operations and arrays and whatnot which involve vector calculations to their
#  corresponding versions with numpy

class calculations:
    lowerLimit = 3E13
    upperLimit = 3.75E14

    def getGravityForce(self, meThing, targetThing, G=6.67E-11):
        """
        Calculates the force of gravity between the two objects. Of course, the force applied on one is the same as the
        force applied on the other. All values inserted in here should be the realistic versions, not the adapted ones.
        :param meThing:
        :param targetThing:
        :param G:
        :return: Vector of the force of gravity between the two objects in that instance
        """
        direction = [(meThing.getRealPosition()[0] - targetThing.getRealPosition()[0]),
                     (meThing.getRealPosition()[1] - targetThing.getRealPosition()[1])]

        distanceSq = direction[0] ** 2 + direction[1] ** 2

        strength = (G * (meThing.mass * targetThing.mass)) / distanceSq

        # We now return the vector of the force of gravity
        return self.getForce(strength, direction)

    def getForce(self, strength, direction):
        """
        Gets a new vector with the same direction but with the magnitude equal to the strength
        :param strength: magnitude we want the vector to be
        :param direction: vector which will tell us the direction we want the new vector to have
        :return: desired vector, with the desired magnitude and the desired direction
        """
        magnitudeDir = self.getMagnitude(direction)
        unitVector = [direction[0] / magnitudeDir, direction[1] / magnitudeDir]
        # print("Unit vector: {:f}, {:f}".format(unitVector[0], unitVector[1]))
        return [unitVector[0] * strength, unitVector[1] * strength]

    def applyAcceleration(self, targetObject: Planet, forceVector: List[int]):
        mass = targetObject.getMass()
        accelerationVector = [forceVector[0] / mass, forceVector[1] / mass]
        targetObject.tugVelocity(accelerationVector)

    def getUnitVector(self, point1: list, point2: list):
        standardVector = self.getStandardVector(point1, point2)
        vectorMagnitude = self.getMagnitude(standardVector)
        return [standardVector[0]/vectorMagnitude, standardVector[1]/vectorMagnitude]

    def getMagnitude(self, standardVector):
        return sqrt(standardVector[0] ** 2 + standardVector[1] ** 2)

    def getStandardVector(self, point1, point2):
        """
        Gets the vector pointing from point1 to point2
        :param point1: starting point
        :param point2: ending point
        :return: vector
        """
        return [point1[0]-point2[0], point1[1]-point2[1]]

    def adjustVelocityToPeriod(self, var, FPS):
        """
        We adjust the velocity to the time interval which has passed since the last "tick". This function expects the
        value to be in m/s, but this will change it to m/period, where period is 1/FPS.
        """
        return var * (1/FPS)

    def adjustVelocityToScreen(self, var):
        """
        We adjust the velocity to what would be representable on screen. We established that 200 pixels/period
        is 150E9 m/period, so 1 m/period is 1.33E-9 pixels/period
        """
        return var * 1.33E-9

    def adjustVelocityCompletely(self, var, FPS):
        """
        Directly adjust to period and screen. Real input, adjusted output.
        :param var:
        :param FPS:
        :return:
        """
        return self.adjustVelocityToScreen(self.adjustVelocityToPeriod(var, FPS))

    def getPerpendicularVector(self, standardVector, clockwise=True, unit=False):
        magnitude = self.getMagnitude(standardVector)
        if(clockwise):
            if(unit):
                return [standardVector[1]/magnitude, -standardVector[0]/magnitude]
            else:
                return [standardVector[1], -standardVector[0]]
        else:
            if(unit):
                return [-standardVector[1]/magnitude, standardVector[0]/magnitude]
            else:
                return [-standardVector[1], standardVector[0]]

    def getClockwise(self, separatingVector, directionVector):
        # We make use of the principles of the cross product
        point = [separatingVector[0] + directionVector[0], separatingVector[1] + directionVector[1]]
        indicator = separatingVector[0]*point[1] - separatingVector[1]*point[0]
        return indicator < 0

    def getCollision(self, object1, object2):
        """
        Determines if there is a collision between two objects. We assume that both objects are circular, since we take
        their radii to determine if they are in contact or not
        :param object1: One of the objects
        :param object2: Another one of the objects
        :return: True if there is a collision, False if not
        """
        position1 = object1.getPosition()
        position2 = object2.getPosition()
        distanceBetweenObjects = math.sqrt((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2)
        radius1 = object1.getRadius()
        radius2 = object2.getRadius()
        sumOfRadii = radius1 + radius2

        return sumOfRadii >= distanceBetweenObjects
