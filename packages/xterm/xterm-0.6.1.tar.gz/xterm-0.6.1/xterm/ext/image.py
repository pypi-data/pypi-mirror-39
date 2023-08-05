from PIL import Image
import xterm.helpers as h
import os

def render_image(filename,size=20,hd=True):
	is_fullscreen = size in ['fullscreen','full','fit']
	terminal_size = os.get_terminal_size()
	im = Image.open(filename)
	#im = im.rotate(270).transpose(Image.FLIP_LEFT_RIGHT)
	pix = im.load()
	imgsize = im.size
	if imgsize[0] > imgsize[1]:
		if is_fullscreen:scalefactor = terminal_size[0]/imgsize[0]
		else:scalefactor = size/imgsize[0]
	else:
		if is_fullscreen:scalefactor = terminal_size[1]/imgsize[1]
		else:scalefactor = size/imgsize[1]
	if hd:
		scalefactorX = (1/scalefactor)/2

		width = (imgsize[0]*scalefactor)
		height = imgsize[1]*scalefactor*2

	else:
		scalefactorX = 1/scalefactor
		width = (imgsize[0]*scalefactor)
		height = (imgsize[1]*scalefactor)

	scalefactorY = 1/scalefactor


	rendered = ''
	fgbefore=()
	colors=[]
	for y in range(int(width)):
		for x in range(int(height)):
			rgb = pix[x*scalefactorX,y*scalefactorY]
			colors.append(rgb)

	i=-1
	if hd:
		while i+1 < len(colors):
			for _ in range(1):
				i+=1
				rgb=colors[i]
				if rgb[3]==255:
					currentfg = h.getrgb(rgb[0],rgb[1],rgb[2])
					if currentfg!=fgbefore:
						rendered+=currentfg
						fgbefore=currentfg
					rendered += '█'
				else:
					rendered+=' '

			if i%(width*2)==0:
				rendered+='\n'


	else:
		while i+1 < len(colors):
			i+=1
			rgb=colors[i]
			if rgb[3]==255:
				currentfg = h.getrgb(rgb[0],rgb[1],rgb[2])
				if currentfg!=fgbefore:
					rendered+=currentfg
					fgbefore=currentfg
				rendered += '██'
			else:
				rendered+='  '
			if i%width==0:
				rendered+='\n'

	#	rendered += '\n'
	return rendered