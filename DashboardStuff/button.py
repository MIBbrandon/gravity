
class button:
	def __init__(self, x, y, width, height, text=''):
		# Colour data is overwritten in the child classes
		self.colour = [130, 130, 130]
		self.deanimatedColour = self.colour
		self.animatedColour = self.colour
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def isOver(self, pos):
		# Pos is the mouse position or a tuple of (x,y) coordinates
		if self.x < pos[0] < self.x + self.width:
			if self.y < pos[1] < self.y + self.height:
				return True
		return False

	def setPosition(self, newPosition):
		self.x = newPosition[0]
		self.y = newPosition[1]

	def animate(self):
		self.setColour(self.animatedColour)

	def deanimate(self):
		self.setColour((self.deanimatedColour))

	def setColour(self, newColour):
		self.colour = newColour
