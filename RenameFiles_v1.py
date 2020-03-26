#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 13:19:26 2020

@author: joiedufranco

The purpose of this script is to rename the collected data from CCP_118 and 
CCP_119 to adhere to the new image file naming system where each acquired image
is PMD_###.##.R##.I##.T## 
- PMD_###.## refers to the unique sample ID number
- R## refers to the specific region of the sample
- I## refers to the specific image acquired of that region

Previously I had used "T##" to denote a different time point of the same 
region. In the new naming system, no "T##" will be specified as it is implied
that each image was taken at a different time point. 

"""
import os
import pandas as pd
import csv

path = "/Users/joiedufranco/Google Drive/Research/MERLIN/Data/CCPs/"
prep = "CCP_118"
pmdid = "PMD_118"

os.chdir(path + prep)
dirlist = os.listdir(os.getcwd())
oldnames = []
newnames = []

# Iterate through all objects in the direction
for x in range(0, 1):#len(dirlist)):
    # Check that the object meets two criteria
    if ((pmdid in dirlist[x]) and not("TL" in dirlist[x])):
        
        # Document the original name
        oldnames.append(dirlist[x])
        
        # Get the sample number
        sample = dirlist[x][8:10]
        
        # Get the location of the original time point #
        tindex = dirlist[x].find("T")
        
        # Assign image number based on time point
        image = dirlist[x][tindex+1:tindex+2]
        
        # Get location of original COI_#
        cindex = dirlist[x].find("COI_")
        
        # Assign region number based on COI_#
        region = dirlist[x][cindex+4:cindex+5]
        
        # Create new name based on gathered information
        basename = pmdid + "." + sample + "." + "R" + region + "." + "I" + image
        
        print(dirlist[x])
        print(basename)
        
        # Document the new name
        newnames.append(basename)
        
        # Go into the folder to rename files
        subpath = path + prep + "/" + dirlist[x]
        os.chdir(subpath)
        
        # Get new list of files
        subdirlist = os.listdir(os.getcwd())
 
        # For every file in the subfolder
        for j in range(0,len(subdirlist)):
            
            # Get channel name
            if ("_C" in subdirlist[j]):
                chindex = subdirlist[j].find("_C")
            elif ("_O" in subdirlist[j]):
                chindex = subdirlist[j].find("_O")     
            
            channel = str(subdirlist[j][chindex+1:len(subdirlist[j])]) 
            print(channel)
            
            # New filename 
            filename = basename + "." + channel
            print(filename)
            
            # Rename file
            os.rename(subdirlist[j], filename)

        # Rename the folder
        os.chdir("..")
        os.rename(dirlist[x], basename)

# Create new dataframe documenting name changes
values = {'Original Name':oldnames, 'Assigned Name':newnames}
dfNames = pd.DataFrame(values)

print(dfNames)
dfNames.to_csv(pmdid + '.NamingConversion.csv')