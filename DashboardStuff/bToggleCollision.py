import pygame

from DashboardStuff.button import button

class bToggleCollsion(button):
	toggle = True

	def __init__(self, x, y, width, height, text=''):
		super().__init__(x, y, width, height, text)
		self.colour = [1, 122, 5]
		self.deanimatedColour = [1, 122, 5]
		self.animatedColour = [2, 201, 9]

	def readjustPosition(self, newDashboardPositionData):
		"""
		We take information that the dashboard has about it's position in order to determine the position that this
		button will take. I intended to place this button in relation to the dashboard, but we are "importing" all of
		data just in case in future moments we want to place the button elsewhere.
		:param newDashboardPositionData List containing info about the position of the dashboard and the screen
		"""
		newScreenDimensions = newDashboardPositionData[0]
		dashboardPosition = newDashboardPositionData[1]
		dashboardWidth = newDashboardPositionData[2]
		dashboardHeight = newDashboardPositionData[3]

		# This the point where you inevitably have to do the math to place the button where you want it
		myNewX = dashboardPosition[0]
		myNewY = dashboardPosition[1] + dashboardHeight - self.height
		self.setPosition([myNewX, myNewY])

	def activate(self, solarSystem):
		self.changeToggle() # Flipping the value of self.toggle
		self.toggleColour() # Changing the animated and deanimated colours of the button to show whether it's off or on
		solarSystem.toggleCollision() # Calling on the solarSystem to turn on/off collision

	def toggleColour(self):
		if(self.toggle):
			self.animatedColour = [2, 201, 9]
			self.deanimatedColour = [1, 122, 5]
		else:
			self.animatedColour = [243, 255, 5]
			self.deanimatedColour = [202, 212, 4]

	def changeToggle(self):
		if(self.toggle):
			self.toggle = False
		else:
			self.toggle = True

	def draw(self, screen, outline=None):
		# Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

		pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), 0)

		if self.text != '':
			font = pygame.font.SysFont('comicsans', 20)
			text = font.render(self.text, 1, (0, 0, 0))
			screen.blit(text, (
			self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))