import pygame

from DashboardStuff.bClearPlanets import bClearPlanets
from DashboardStuff.bToggleCollision import bToggleCollsion


class dashboard:

	alreadyPressed = False
	shiftPressed = False

	def __init__(self, solarSystem):
		self.solarSystem = solarSystem
		self.colour = [6, 4, 36]
		x, y = pygame.display.get_surface().get_size()
		self.width = x
		self.height = 115
		self.position = [0, y-self.height]
		clearPlanets = bClearPlanets(0, 0, 290, 70, "Clear planets")
		toggleCollision = bToggleCollsion(0, 0, 150, 70, "Toggle Collision")
		self.buttons = [clearPlanets, toggleCollision]

	def exist(self):
		self.animateAndActivate()

	def draw(self, screen):
		# Drawing the rectangle which houses all the buttons
		pygame.draw.rect(screen, self.colour, (self.position[0], self.position[1], self.width, self.height), 0)

		# Drawing all of the buttons on the dashboard
		for button in self.buttons:
			button.draw(screen, True)

	def animateAndActivate(self):
		# When said button is pressed, apply it's intended action
		mousePosition = pygame.mouse.get_pos()
		pressed = pygame.mouse.get_pressed()[0]
		for button in self.buttons:
			if(button.isOver(mousePosition)):
				button.animate()
				if(pressed and not self.alreadyPressed):
					self.alreadyPressed = True
					button.activate(self.solarSystem)
			else:
				button.deanimate()
		self.updateAlreadyPressed()

	def readjustPositions(self, newScreenDimensions):
		x, y = newScreenDimensions[0], newScreenDimensions[1]
		self.width = x
		self.height = 115
		self.position = [0, y-self.height]
		newDashboardPositionData = [newScreenDimensions, self.position, self.width, self.height]
		for button in self.buttons:
			# Now we want to readjust the position of button in relation to the dashboard
			button.readjustPosition(newDashboardPositionData)

	def updateAlreadyPressed(self):
		"""
		If the left click is no longer being pressed, alreadyPressed goes to false
		"""
		if (not pygame.mouse.get_pressed()[0]):
			self.alreadyPressed = False

	def isOver(self, pos):
		# Pos is the mouse position or a tuple of (x,y) coordinates
		if self.position[0] < pos[0] < self.position[0] + self.width:
			if self.position[1] < pos[1] < self.position[1] + self.height:
				return True
		return False
