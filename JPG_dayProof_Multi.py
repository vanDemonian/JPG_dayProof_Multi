#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
Filename:           JPG_dayProofSheet.py
Author:             Martin Walch
Release Date:       2015-05-12
Description:        HI-Res multi-format version of JPG_dayProofer.py
                    
            ****    No gaps between thumbnails  *****
                    


                    Iterates through a directory tree of JPG's renamed by JPG_reNamer.py.

                    TARONGA_2014_09_29-11_56_58.jpg

                    Creates a new sheet for each date and places each thumbnail according to
                    the time of day it was taken. 
                    Also creates a log file and saves it to same destination as Proofs.

            ****    format:     2 = FullFrame,  1 = Portrait,   0 = Landscape

            ****    paperSize:   in pixels (width, height)
                    
                    4K resolution, as defined by Digital Cinema Initiatives, is 4096 x 2160 pixels (256:135, approximately a 1.9:1 aspect ratio)
                    Standard Nikon D3200 File = 4512 x 3000  (width by height)
                    therefore       width     = 1.504 x height
                                    height    = 0.665 x width
                    
                    
                    OUTPUT VARIABLES

                    Portrait Format
                    14 columns  (12 images + left & right border)
                    26 rows     (24 images + top and bottom border)
            


Required Modules:  

                    logWriter.py
                    cellData.py
                    proofSheet.py
---------------------------------------------------------------------------------------------------
"""






import glob
from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from PIL.ExifTags import TAGS, GPSTAGS
import string, sys, traceback, datetime, time, calendar
import os, shutil
from PIL import *
import math
from cellData_dayProofMulti import *
from multiprocessing import Pool
from proofSheet_Multi import *


#portrait formats
"""
P_A3at150dpi    = (1750, 2158)
P_A3thumb       = (125, 83)
P_A3 = P_A3at150dpi

P_A2at150dpi    = (2464, 3042)
P_A2thumb       = (176, 117)
P_A2 =P_A2at150dpi

P_A1at150dpi    = (3500, 4316)
P_A1thumb       = (250, 166)
P_A1 = P_A1at150dpi

P_A0at150dpi    = (4956, 6110)
P_A0thumb       = (354, 235)
P_A0 = P_A0at150dpi
"""



inputDir = '/Users/pyDev/Documents/JPG_dayProofer_Multi/JPG_proof_Inputs'   #root directory that will be parsed (includes subdirectories)
#outputDir = '/Users/pyDev/Documents/JPG_dayProofer_Multi/JPG_proof_Outputs' #output directory (must be created before script is run)
fileExt = '.jpg'
#cameraInterval = 300 #this is the number of seconds between each capture:   5mins = 300 secs


nameList = []
namePath = []
dateList = []
cellInfo = []


DateChangeList =[]

DAYS = []



count = 0



def Timer(start, end):
    """
    Calculates the time it takes to run a process, based on start and finish times
    ---------------------------------------------------------------------------------------------
    Inputs:       in seconds 
    start:        Start time of process
    end:          End time of process
    ---------------------------------------------------------------------------------------------
    """
    elapsed = end - start
    # Convert process time, if needed
    if elapsed <= 59:
        time = str(round(elapsed,2)) + " seconds\n"
    if elapsed >= 60 and elapsed <= 3590:
        min = elapsed / 60
        time = str(round(min,2)) + " minutes\n"
    if elapsed >= 3600:
        hour = elapsed / 3600
        time = str(round(hour,2)) + " hours\n"
    return time





##### RUN #####

if __name__ == '__main__':
    #start = time.clock()
    start = time.time()

    print '   '
    print 'JPG_dayProofSheet.py   '
    print '   '

    # loop to create list of names and paths
    for root, dirs, files in os.walk(inputDir):
        for name in files:
            
            if name.endswith(fileExt):

                nameList.append(name)           #list of filenames - basename only
                namePath.append(os.path.join(root,name))    #list of names with directory paths

                count = count + 1

    #---------------------------------------------------------------
    #print namePath - debug

    #set date of first name as today and appends it to the start of 'dateList'
    todaysdate = nameList[0][8:18]
    dateList.append(todaysdate)
    #print dateList - debug

    #   loop to create list of days by checking if the date changes
    #   and adding the date to the list of dates it does.
    for name in nameList:

        if name[8:18] != todaysdate:
            #create new day and append name
            dateList.append(name[8:18])
            #make the new date = 'today'
            todaysdate = name[8:18]



    numberofDays = len(dateList)
    print 'Number of Days = ', numberofDays

    #---------------------------------------------------------------

    today = 0

    for i in range(0,len(namePath)):
        date = os.path.basename(namePath[i])
        date = date[8:18]
        

        if date != today:
            today = date
            DateChangeList.append(i)
        
        print ' ', i,'   ',date

    DateChangeList.append(len(namePath)-1)
    print 'Date Change List  ', DateChangeList


    #---------------------------------------------------------------



    d = 0

    for x in range(len(DateChangeList)-1):
        #print x,' ', len(namePath)
        v = DateChangeList[d]
        
        v1 =DateChangeList[(d+1)]
        print 'v ',v,'v1 ',v1
        proofPath = namePath[v:v1]
        DAYS.append(proofPath)





        d+=1


    pool = Pool()
    pool.map(proofSheet, DAYS )
    pool.close()
    pool.join()

    print ' '
    print ' '
    print ' '

   




    finish = time.time()



    print 'List of dates in data', dateList
    print 'Total Number of dates = ', len(dateList)
    print 'Total Number of Images processed: ', str(count)
    print 'Processing done in ', Timer(start, finish), '\n'






