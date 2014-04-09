from graphics import *
from random import *

#need to set gameWidth and gameHeight in order to use this module!!
gameHeight = 260
gameWidth = 320
NONE, TOP, RIGHT, BOTTOM, LEFT = 0, 10, 20, 30, 40
DOUBLEBALL = 110
#also need a window object to pass to the classes
#it looks like this: 
#win = GraphWin("Paddle Game", gameWidth*3, gameHeight*3)
#win.setCoords(0, 0, gameWidth, gameHeight)


class Block:

	def __init__(self, win, center, width, height):
		#takes win, bottomleft(a point), height, and width, as arguments
		self.win = win
		self.center = center
		self.height = height
		self.halfheight = height / 2
		self.width = width
		self.halfwidth = width / 2

		self.tr = Point(center.getX()+self.halfwidth, center.getY()+self.halfheight)
		self.bl = Point(center.getX()-self.halfwidth, center.getY()-self.halfheight)

		self.special = NONE

		self.o = Rectangle(self.bl, self.tr)

		self.r, self.g, self.b = 255, 255, 255
		self.rgb = color_rgb(255, 255, 255)

		self.o.setFill(self.rgb)

		self.active = 1

	def draw(self):
		self.o.draw(self.win)

	def undraw(self):
		self.o.undraw()			

	def activate(self):
		self.active = 1

	def deactivate(self):
		self.active = 0

	def kill(self):
		self.o.undraw()
		self.deactivate()

	def getCenter(self):
		return self.center

	def getBottomLeft(self):
		return self.bl

	def getTopRight(self):
		return self.tr

	def isActive(self):
		return self.active

	def setSpecial(self, s):
		self.special = s
		if s == DOUBLEBALL:
			self.setColor(color_rgb(255, 0, 0))

	def setNormal(self):
		self.special = NONE

	def isSpecial(self):
		return self.special

	def setColor(self, c):
		self.o.setFill(c)


class Paddle:

	#object must be passed a window object
	#x1, y1, x2, y2 are the bottom left, and top right coordinates
	#top is the top of the paddle, given in pixels
	def __init__(self, win, width, height, bottom, gameWidth):
		self.win = win

		self.bottom = bottom
		self.top = bottom+height
		
		self.height = height
		self.halfheight = self.height / 2
		self.width = width
		self.halfwidth = self.width / 2

		self.center = gameWidth / 2
		
		self.o = Rectangle(Point(self.center-self.halfwidth, bottom), Point(self.center+self.halfwidth, bottom+height))
		self.o.setFill(color_rgb(255, 255, 255))

		self.center = self.o.getCenter().getX()
		self.startCenter = self.center

		self.maxX = gameWidth - self.halfwidth
		self.minX = 0 + self.halfwidth

		self.maxSpeed = 2

		self.xdest = self.center

	def draw(self):
		self.o.draw(self.win)

	def undraw(self):
		self.o.undraw()

	def hide(self):
		self.reset()
		self.o.undraw()

	def show(self):
		self.reset()
		self.o.draw(self.win)

	def reset(self):
		self.o.move(self.startCenter - self.center, 0)
		self.center = self.startCenter
		self.xdest = self.startCenter

	def getLeft(self):
		return self.center - self.halfwidth

	def getRight(self):
		return self.center + self.halfwidth

	def getTop(self):
		return self.bottom+self.height

	def getBottom(self):
		return self.bottom

	def getBottomLeft(self):
		p = Point(self.getLeft(), self.bottom)
		return p

	def getTopRight(self):
		p = Point(self.getRight(), self.bottom + self.height)
		return p

	def setMaxSpeed(self, s):
		self.maxSpeed = s + (s*.3)

	def setDest(self, xDest):
		if xDest > self.maxX:
			xDest = self.maxX
		elif xDest < self.minX:
			xDest = self.minX
		self.xdest = xDest

	def update(self):
		self.center = self.o.getCenter().getX()
		if self.xdest <= self.center - self.maxSpeed:
			self.o.move(-self.maxSpeed, 0)
		elif self.xdest >= self.center + self.maxSpeed:
			self.o.move(self.maxSpeed, 0)

class Ball:

	#object must be passed a window object
	#window object to draw in, x and y starting coords, radius, and whether it can destroy blocks (true or false)
	def __init__(self, win, x, y, radius, p):
		self.x = x
		self.y = y
		self.radius = radius
		#initialize x velocity
		self.xvel = random() * .8
		#randomly set the x velocity to its opposite
		if random() < .5:
			self.xvel *= -1 
		self.yvel = -1
		#variables to determine where the ball bounces off the walls
		self.maxX = gameWidth
		self.maxY = gameHeight
		self.o = Circle(Point(self.x, self.y), self.radius)
		self.win = win
		self.o.setFill(color_rgb(255, 255, 255))
		self.stopped = 0
		#set whether or not it destroys blocks
		if p:
			self.powerful()
		else:
			self.powerless()
		self.active = 1

	def draw(self):
		self.o.draw(self.win)

	def undraw(self):
		self.o.undraw()

	def kill(self):
		self.undraw()
		self.freeze()
		self.powerless()
		self.deactivate()

	def go(self):
		self.stopped = 0

	def freeze(self):
		self.stopped = 1

	def isStopped(self):
		return self.stopped

	def powerful(self):
		self.power = 1
		self.o.setFill(color_rgb(255, 255, 255))

	def powerless(self):
		self.power = 0
		self.o.setFill(color_rgb(255, 0, 0))

	def isPowerful(self):
		return self.power

	def activate(self):
		self.active = 1

	def deactivate(self):
		self.active = 0

	def isActive(self):
		return self.active

	def goRight(self):
		self.xvel = abs(self.xvel)

	def goLeft(self):
		self.xvel = (abs(self.xvel)) * -1

	def goUp(self):
		self.yvel = abs(self.yvel)

	def goDown(self):
		self.yvel = (abs(self.yvel)) * -1

	def getXvel(self):
		return self.xvel

	def reverseX(self):
		self.xvel = self.xvel * -1

	def reverseY(self):
		self.yvel = self.yvel * -1

	def addRandom(self):
		#randomize the speed of the ball
		#store the velocities temporarily, to keep them from going the opposite way
		tempXvel = self.xvel
		tempYvel = self.yvel

		#change the speed more randomly if the ball isn't killing blocks
		if self.isPowerful():
			#random numbers between 0 and .2 (adjust with the divisor)
			r = random() / 5
			r2 = random() / 5
			if self.xvel > 0:
				self.xvel += r
			else:
				self.xvel -= r
			if self.yvel > 0:
				self.yvel += r2
			else:
				self.yvel -= r2
		else:
			r = (random() -.5) / 6
			r2 = (random() -.5) / 6
			self.xvel += r
			self.yvel += r2
		

	def capSpeed(self):
		#make sure it doesn't go too fast (2) (but still keep randomness)
		r = random() / 8
		if self.xvel > 2:
			self.xvel = 2+r
		if self.xvel < -2:
			self.xvel = -2-r
		if self.yvel > 2:
			self.yvel = 2+r
		if self.yvel < -2:
			self.yvel = -2-r
		#or too slow (.35)
		if self.xvel > 0 and self.xvel < .35:
			self.xvel = .35+r
		if self.xvel < 0 and self.xvel > -.35:
			self.xvel = -.35-r
		if self.yvel > 0 and self.yvel < .35:
			self.yvel = .35+r
		if self.yvel < 0 and self.yvel > -.35:
			self.yvel = -.35-r

	def getBottomLeft(self):
		return self.o.getP1()

	def getTopRight(self):
		return self.o.getP2()

	def checkWallBounce(self):
		#bounce off the walls...this should be reworked, perhaps
			if self.x + self.radius >= self.maxX or self.x - self.radius <= 0:
				self.reverseX()
			if self.y + self.radius >= self.maxY:
				#ball gains power when hitting the top wall
				self.reverseY()
				self.powerful()

	def checkOutOfBounds(self):
		if self.y - self.radius <= 0:
			self.freeze()
			self.powerless()
			self.deactivate()
			self.o.undraw()

	def update(self):
		#if the ball is active
		if not self.isStopped():
			self.checkWallBounce()
			#stop the ball if it hits the bottom...this needs to be changed
			self.checkOutOfBounds()
			self.x = self.x + self.xvel
			self.y = self.y + self.yvel
			self.o.move(self.xvel, self.yvel)

