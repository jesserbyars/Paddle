from msvcrt import *
from time import sleep

from paddleobjects import *

#GLOBAL VARIABLES
#pseudo constants for the sides, ballsize, and collision offset
wallWidth = 3
ballSize = 3
collisionOffset = 0

#create the graphics window
win = GraphWin("Paddle Game", gameWidth*3, gameHeight*3)
win.setCoords(0-wallWidth, 0-wallWidth, gameWidth+wallWidth, gameHeight+wallWidth)
win.setBackground(color_rgb(0, 0, 0))

pad = Paddle(win, 50, 5, 0, gameWidth)
pad.draw()

#initialize ball and block lists
ballList = []
blockList = []


#FUNCTIONS

def buildWalls():
	leftWall = Rectangle(Point(0-wallWidth, 0), Point(0, gameHeight))
	leftWall.setFill(color_rgb(255, 255, 255))
	leftWall.draw(win)
	rightWall = Rectangle(Point(gameWidth, 0), Point(gameWidth+wallWidth, gameHeight))
	rightWall.setFill(color_rgb(255, 255, 255))
	rightWall.draw(win)
	topWall = Rectangle(Point(0-wallWidth, gameHeight), Point(gameWidth+wallWidth, gameHeight+wallWidth))
	topWall.setFill(color_rgb(255, 255, 255))
	topWall.draw(win)

def addBall(loc, size, p):
	#takes size, a Point object with starting location to initialize, and True or False for power to destroy blocks
	tempObj = Ball(win, loc.getX(), loc.getY(), size, p)
	tempObj.draw()
	ballList.append(tempObj)

def addBlock(center, width, height, c):
	#bottomleft (as a point), width, and height, and c(color)
	tempObj = Block(win, center, width, height)
	tempObj.setColor(c)
	tempObj.draw()
	blockList.append(tempObj)

def waitForClick(s):
	tempText = Text(Point(gameWidth/2, gameHeight/2 - 40), s)
	tempText.setFill(color_rgb(255, 255, 255))
	tempText.draw(win)
	nothing = win.getMouse()
	tempText.undraw()
	
def makeStartingBall():
	addBall(Point(gameWidth/2, (gameHeight/2)-10), ballSize, True)

def getBlocksLeft():
	num = 0
	for b in blockList:
		if b.isActive():
			num += 1
	return num

def getBallsLeft():
	num = 0
	for b in ballList:
		if b.isPowerful():
			num += 1
	return num

def checkCollide(bl1, tr1, bl2, tr2):
	#checks to see if object1 collided with object2, on WHICH side of object 2

	oneLeft = bl1.getX()
	oneRight = tr1.getX()
	oneBottom = bl1.getY()
	oneTop = tr1.getY()
	twoLeft = bl2.getX()
	twoRight = tr2.getX()
	twoBottom = bl2.getY()
	twoTop = tr2.getY()

	if oneLeft >= twoRight+collisionOffset or oneRight <= twoLeft-collisionOffset or oneBottom >= twoTop+collisionOffset or oneTop <= twoBottom-collisionOffset:
		return False, NONE, NONE
	else:
		#this part is no longer completely broken...
		xside = NONE
		yside = NONE
		if twoRight - oneLeft <= 15:
			xside = RIGHT
			print("RIGHT!")
		elif oneRight - twoLeft  <= 15:
			xside = LEFT
			print("LEFT!")
		if twoTop - oneBottom <= 2:
			yside = TOP
			print("TOP!")
		elif oneTop - twoBottom <= 2:
			yside = BOTTOM
			print("BOTTOM!")
		return True, xside, yside

def blockRow(y, amount, height, spacing, c):
	#y is the y location for the row, amount is the qty of blocks per row, height is how tall the blocks are, and spacing is the offset on the sides of the block, c is a color_rgb object
	#send -1 to the c parameter for a random color
	bw = gameWidth // amount
	if c == -1:
		r = randrange(20, 235)
		g = randrange(20, 235)
		b = randrange(20, 235)
		c = color_rgb(r, g, b)
	#bw is block width, determined by dividing the game width by the amount of blocks
	#this formula *usually* works, but should be tested with different widths of screen and blocks
	for i in range(bw//2, gameWidth, bw):
		addBlock(Point(i, y), bw-spacing, height, c)

def buildLevel(l):
	#create different levels and load them by the l parameter
	#trust the formula, or tweak it, just don't ask
	blockList = []
	ballList = []
	closeness = gameHeight // 12
	if l == 1:		
		for x in range(2):
			blockRow(gameHeight - closeness*(x+1), 6, 5, 1, -1)
	elif l == 2:
		for x in range(5):
			blockRow(gameHeight - closeness*(x+1), 8, 5, 1, -1)
	elif l == 3:
		for x in range(6):
			blockRow(gameHeight - closeness*(x+1), 10, 5, 1, -1)
	makeSpecials()

def makeSpecials():
	#assigns random blocks to be special blocks
	for b in blockList:
		if random() < .1:
			b.setSpecial(DOUBLEBALL)

def weakBall(p, s):
	#creates a ball that can't break blocks
	#point and size are the parameters
	addBall(p, s, False)	

def getMaxSpeed():
	#returns the max speed of all of the active balls (2 minimum)
	ms = 0
	for c in ballList:
		t = c.getXvel()
		if t > ms:
			ms = t
	if ms < 2:
		ms = 2
	return ms
		

def main():
	
	currentLevel = 1
	buildWalls()
	waitForClick("Level " + str(currentLevel) + "\n\n Click to Continue")
	makeStartingBall()

	while True:

		buildLevel(currentLevel)

		#temporary powerless ball at the top
		#weakBall(Point(gameWidth/2, gameHeight - 35), ballSize)
		
		#while there are still blocks active in the current level
		while getBlocksLeft() > 0:
			#resets the paddle and waits for a click if there are no active balls
			if(getBallsLeft() == 0):
				pad.reset()
				win.checkMouse()	
				waitForClick("Click to Continue...")
				makeStartingBall()
		
			#stop the program from running too fast
			sleep(.005)
			#check for a mouse click without pausing
			click = win.checkMouse()
			#handle a mouseclick here for moving the paddle()
			if click:
				#set the destination for the paddle
				pad.setDest(click.getX())

			#do updates for the balls here			
			for c in ballList:
				if c.isActive():
					#move the ball according to it's velocity if it's active		
					c.update()
					#check for a collision with the paddle
					collision, xside, yside = checkCollide(c.getBottomLeft(), c.getTopRight(), pad.getBottomLeft(), pad.getTopRight())
					#if the ball hits the paddle
					if(collision):
						if yside == TOP or yside == NONE:
							c.goUp()
						if xside == LEFT or xside == RIGHT:
							if xside == LEFT:
								c.goLeft()
							if xside == RIGHT:
								c.goRight()
						

			#do updates for the paddle here
			pad.update()

			#keep the paddle able to move as fast as the fastest ball, 2 min
			pad.setMaxSpeed(getMaxSpeed())

			#check for block collisions here
			for c in ballList:
				for bl in blockList:
					if bl.isActive() and c.isActive():
						collision, xside, yside = checkCollide(c.getBottomLeft(), c.getTopRight(), bl.getBottomLeft(), bl.getTopRight())
						if(collision):
							#add randomness to the velocity of the ball
							c.addRandom()
							#caps the speed of the ball
							c.capSpeed()
							#turn the block inactive if the ball is powerful
							if c.isPowerful():
								if bl.isSpecial()==DOUBLEBALL:
									addBall(bl.getCenter(), ballSize, True)
								bl.kill()

							#add logic for reversing the direction
							if yside == TOP or yside == NONE:
								c.goUp()
							elif yside == BOTTOM:
								c.goDown()
															
							elif xside == NONE and yside == NONE:
								print("NONE!!!")
								c.goUp()

		pad.reset()
		for b in ballList:
			b.kill()

		currentLevel += 1
		waitForClick("Level " + str(currentLevel) + "\n\n Click to Continue")
		makeStartingBall()

		#wait for a click
		#click = win.getMouse()
		#win.close()

if __name__ == "__main__":
	main()
