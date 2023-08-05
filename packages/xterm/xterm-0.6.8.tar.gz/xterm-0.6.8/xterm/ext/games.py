'''
still in development, you probably shouldn't use this yet




makes making games in the terminal a whole lot easier




'''

import xterm.main as xterm
import xterm.helpers as h
#from . import async as xterm
from threading import Thread,Timer
import time

class data:
	objects = []
class pixel:
	def __init__(self,letter,modifier,x,y):
		self.letter=letter
		self.modifier=modifier
		self.x=x
		self.y=y
class positionQueue:
	def __init__(self):
		self.queue = []
	def add(self,item):
		self.queue.append(item)
		data.x+=1

#queue=[]
#def addtoqueue


def frame():
	while True:
		starttime=time.time()
		for o in data.objects:
			print(o[1])
			for p in o[0].points:
				print(p)
		endtime=time.time()
		time.sleep((endtime-starttime)+1/data.fps)

def start(fps=5):
	data.fps = fps
	Thread(target=frame).start()

class ascii_object:
	def __init__(self,points):
		self.points = points
def create_object(*points):
	return ascii_object(points)
def place_object(obj,coords=(0,0)):
	data.objects.append((obj,coords))
	return obj