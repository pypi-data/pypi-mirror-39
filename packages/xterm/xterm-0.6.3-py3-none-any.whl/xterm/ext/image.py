from PIL import Image
import xterm.helpers as h
import os

def render_image(filename,size=20):
	if size in ['fullscreen','full','fit']:
		size = os.get_terminal_size()[0]
	im = Image.open(filename)
	im = im.rotate(270).transpose(Image.FLIP_LEFT_RIGHT)
	pix = im.load()
	imgsize = im.size
	if imgsize[0] > imgsize[1]:
		scalefactor = size/imgsize[0]
	else:
		scalefactor = size/imgsize[1]
	scalefactor2 = 1/scalefactor

	width = imgsize[0]*scalefactor
	height = imgsize[1]*scalefactor

	rendered = ''
	fgbefore=()
	colors=[]
	for x in range(int(width)):
		for y in range(int(height)):
			rgb = pix[x*scalefactor2,y*scalefactor2]
			#x,y,rgb
			if rgb[3]==255:
				currentfg = h.getrgb(rgb[0],rgb[1],rgb[2])
				if currentfg!=fgbefore:
					rendered+=currentfg
					fgbefore=currentfg
				rendered += '██'
			else:
				rendered+='  '
		rendered += '\n'
	print(rendered)