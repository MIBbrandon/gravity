import time

import pygame
import os
from pathlib import Path

import config
from Utils.calculations import calculations
from math import *


class Planet:
	base_path = Path(os.path.dirname(__file__)).parent
	image_width = 10
	image_height = 10

	c = calculations()

	def __init__(self, screen, name, position, velocity, radius, mass, colour=None):
		self.id = -1
		self.screen = screen
		self.name = name
		self.planet_sprite_path = os.path.join(self.base_path, 'sprites', self.name+'.png')
		self.position = position
		# 200 pixels are 150E9 m, so 1 pixel is 7.5E8.
		self.realPosition = [position[0] * 7.5E8, position[1] * 7.5E8]
		self.velocity = velocity
		self.realVelocity = [velocity[0] * 7.5E8, velocity[1] * 7.5E8]
		self.speed = ceil(sqrt(velocity[0] ** 2 + velocity[1] ** 2))  # ceil() so that speed=1 unless velocity=[0,0]
		self.realSpeed = sqrt(self.realVelocity[0] ** 2 + self.realVelocity[1] ** 2)
		self.radius = radius
		self.colour = [255, 255, 255]
		self.mass = mass
		self.image = pygame.image.load(self.planet_sprite_path)
		self.image_width, self.image_height = self.image.get_size()


	def move(self):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]

	def realMove(self):
		self.setRealPosition(self.realPosition[0]+(self.realVelocity[0]*(1/config.FPS)*config.velocityIncrease),
							 self.realPosition[1]+(self.realVelocity[1]*(1/config.FPS)*config.velocityIncrease))



	def setRealVelocity(self, x, y):
		self.realVelocity = [x, y]
		self.setVel(self.realVelocity[0] / config.kmPerPixel, self.realVelocity[1] / config.kmPerPixel)

	def setVel(self, x, y):
		self.velocity = [x, y]

	def tugVelocity(self, acceleration):

		pygame.draw.line(self.screen, [237, 26, 223],
						 [self.position[0],
						  self.position[1]],
						 [(self.position[0] + acceleration[0]*1E4),
						  (self.position[1] + acceleration[1]*1E4)], 4)
		self.setRealVelocity(self.realVelocity[0] + acceleration[0]*config.accelerationIncrease,
							 self.realVelocity[1] + acceleration[1]*config.accelerationIncrease)


	def setRealPosition(self, x, y):
		self.realPosition = [x, y]
		self.position = [self.realPosition[0] / config.kmPerPixel, self.realPosition[1] / config.kmPerPixel]

	def setPosition(self, x, y):
		self.position = [x, y]
		self.realPosition = [self.position[0] * config.kmPerPixel, self.position[1] * config.kmPerPixel]

	def getRealPosition(self):
		return self.realPosition

	def getPosition(self):
		return self.position

	def getRadius(self):
		return self.radius

	def getMass(self):
		return self.mass

	def attract(self, astralObjects, velocityIncrease):
		pass
		# for object in astralObjects:
		# 	if object.id != self.id and object.id != 0:  # Not attracting itself nor the sun
		# 		gravityForce = self.c.getGravityForce(self, object)
		# 		self.c.applyAcceleration(object, gravityForce)


	def stabilizeOrbit(self, solarSystem):
		"""
        Adjusts the planet's velocity to put it in a stable orbit in relation to the sun
        :param solarSystem
        """
		# We know that in order to have a stable orbit, the gravitational force must be equal to the centripetal force.
		# So, G*M1*m2/(r^2)=m2*(v^2)/r, and solving for v, we get v = sqrt(G*M1/r)

		# So now, we obtain G
		G = solarSystem.getGravitationalConstant()

		#print("G: " + str(G))

		# Now M1
		M1 = solarSystem.sun.getMass()

		#print("M1: " + str(M1))

		# And finally, r (we also want rVector to calculate the direction in which we must apply the velocity, which
		# must of course be perpendicular to rVector)
		realRVector = self.c.getStandardVector(self.realPosition, solarSystem.sun.getRealPosition())
		# print("Planet real position: (" + str(self.realPosition[0])
		# 	  + ", " + str(self.realPosition[1]) + ")")
		# print("Sun real position: (" + str(solarSystem.sun.getRealPosition()[0])
		# 	  + ", " + str(solarSystem.sun.getRealPosition()[1]) + ")")

		realR = self.c.getMagnitude(realRVector)
		# print("Real r: " + str(realR))

		# With all of this, let's now get v
		realV = sqrt(G * M1 / realR)
		# print("Real v: " + str(realV))

		unitRVector = self.c.getUnitVector(self.realPosition, solarSystem.sun.getRealPosition())

		perpendicularVector = self.c.getPerpendicularVector(unitRVector, True, True)

		# Now for the complete stable velocity vector
		stableRealVelocity = [realV*perpendicularVector[0], realV*perpendicularVector[1]]

		# Now we must set this velocity as our current one
		self.setRealVelocity(stableRealVelocity[0], stableRealVelocity[1])

	def checkCollision(self, astralObjects):
		for object in astralObjects:
			if (object.id != self.id and self.c.getCollision(self, object)):
				return True
		return False

	def updateFPS(self, FPS):
		self.FPS = FPS

	def draw(self):
		# pygame.draw.circle(self.screen, self.colour, self.position, self.radius)
		# pygame.draw.rect(self.screen, self.colour,
		# [self.position[0] - self.radius, self.position[1] - self.radius, self.radius, self.radius])
		self.screen.blit(self.image, [self.position[0] - (self.image_width / 2), self.position[1] - (self.image_height / 2)])
		# Now we want a velocity vector
		if (self.name == "mercury"):
			self.colour = [255, 0, 255]
		elif (self.name == "venus"):
			self.colour = [0, 250, 0]
		elif (self.name == "earth"):
			self.colour = [10, 200, 210]
		elif(self.name == "mars"):
			self.colour = [150,0,0]
		elif (self.name == "jupiter"):
			self.colour = [150, 80, 0]
		elif (self.name == "saturn"):
			self.colour = [150, 0, 10]
		elif (self.name == "uranus"):
			self.colour = [150, 0, 150]
		elif (self.name == "neptune"):
			self.colour = [0, 0, 150]
		# pygame.draw.line(self.screen, self.colour,
		# 				 [self.position[0],
		# 				  self.position[1]],
		# 				 [(self.position[0] + self.velocity[0]*1E6),
		# 				  (self.position[1] + self.velocity[1]*1E6)])
