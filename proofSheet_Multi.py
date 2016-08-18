#!/usr/bin/python
import glob
from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from PIL import ImageFont
from PIL import ImageDraw
from PIL.ExifTags import TAGS, GPSTAGS
import string, sys, traceback, datetime, time, calendar
import os, shutil
from PIL import *
import math
from cellData_dayProofMulti import *

outputDir = 'JPG_proofOutputs'


def proofSheet(DAY):

	'Creates a proofsheet from a list of JPGs'

	backGround = (255,255,255)
	paperSize = (1750, 2158)
	thumbSize = (125, 83)
	quality = 100


	if os.path.isdir(outputDir) != 1:
            os.mkdir(outputDir)

	cellInfo = []
	today = os.path.basename(DAY[0])
	
	location = today[0:7]
	today = today[8:18]
	
	print '\ntoday ', today
	print ' '


	#create new Proof.tiff file
	Proofimg = Image.new('RGB', paperSize, backGround)

	
	fnt = ImageFont.truetype('TrueTypeFonts/arial.ttf', 30)

	#process all thumbs from day
	for name in DAY:

	
		#resize
		img = Image.open(name).resize(thumbSize)
		name = os.path.basename(name)
		#parse cellInfo
		nameInfo = cellNumbers(name) # call to cellNUmbers function that delivers info for each image in proof set 
		cellInfo.append(nameInfo) #list of cellInfo for each cell

   		Proofimg.paste(img,(nameInfo[12][0],nameInfo[12][1]))

   	#add the date as text
   	draw = ImageDraw.Draw(Proofimg)
   	draw.text((125, 30), location, font=fnt, fill=(0,0,0,128))
	draw.text((1460, 30), today, font=fnt, fill=(0,0,0,128))



   	#Proofimg.save(outputDir+'/'+nameInfo[2] +'_'+ today +'_'+'PROOF_'+'.tif','tiff', quality=quality)#tiff
   	Proofimg.save(outputDir+'/'+nameInfo[2] +'_'+ today +'_'+'PROOF_'+'.jpeg','jpeg', quality=100)#jpeg
	

	print 'cellInfo ',cellInfo

	



