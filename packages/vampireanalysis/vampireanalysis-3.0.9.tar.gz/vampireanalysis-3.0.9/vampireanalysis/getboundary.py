#!/usr/bin/env python

# built-in libraries
import os
from time import sleep
import re
# external libraries
from PIL import Image
from scipy.ndimage.measurements import center_of_mass, label
from scipy.ndimage import generate_binary_structure
import numpy as np
import cv2
import pandas as pd

def createimstack(ch,setfolder):
	imlist = [_ for _ in os.listdir(setfolder) if _.lower().endswith('.tiff')]
	imlist = [_ for _ in imlist if re.split('_+',_)[0].lower() == ch.lower()] 	##fixpoint
	#imlist.sort(key=lambda f: int(filter(str.isdigit,f)))
	imlist = sorted(imlist)
	imlistpath = [os.path.join(setfolder,_) for _ in imlist]
	imstack = [np.array(Image.open(im)) for im in imlistpath]
	return imstack,imlistpath,imlist

def check_label_status(im):
	imlabel = list(set(im.flatten()))[1:]
	if len(imlabel) > 1: tag='labeled'
	return tag

def mask2boundary(mask):
	im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contour = np.empty(2)
	for i in range(len(contours[0])):
		contour = np.vstack((contours[0][i][0],contour))
	contour=contour[0:-1]
	contour.T[0] = contour.T[0]+1
	contour.T[1] = contour.T[1]+1
	boundary = np.empty((2,len(contour.T[1])))
	boundary[0] = contour.T[1]
	boundary[1] = contour.T[0]
	boundary = boundary.T.astype(int)
	return boundary

def getboundary(folder,progress_bar):
	sets = [_ for _  in os.listdir(folder) if os.path.isdir(os.path.join(folder,_))]
	setpaths = [os.path.join(folder,_) for _ in sets]
	for setfolderidx, setfolder in enumerate(setpaths):
		progress_bar["value"] = 100*setfolderidx/len(setpaths)
		progress_bar.update()
		UI = pd.read_csv(os.path.join(folder,'Image set ledger.csv'))
		ch1= UI['ch1'][setfolderidx]
		ch2= UI['ch2'][setfolderidx]
		chlist = [ch1,ch2]
		for ch in chlist:
			imstack,imlistpath,imlist = createimstack(ch,setfolder)
			inputim = check_label_status(imstack[0]) 
			if inputim is not 'labeled':
				s = generate_binary_structure(2,2)
				imstack = [label(im,structure=s)[0] for im in imstack]
			cmasses=[]
			cmassdst = os.path.join(setfolder,ch+'_centroid.pickle')
			boundarymaster=[]
			boundarydst = os.path.join(setfolder,ch+'_boundary_coordinate_stack.pickle')
			for imidx, im in enumerate(imstack):
				labels = list(set(im.flatten()))[1:]
				for objidx,lab in enumerate(labels):
					mask = np.array((im==lab).astype(int),dtype='uint8')
					if not os.path.exists(cmassdst):
						cmass = [int(np.around(_,0)) for _ in center_of_mass(mask)]
						cmass.reverse()
						area = [int(np.sum(mask))]
						fronttag = [imlist[imidx],imidx+1,objidx+1]
						cmass = fronttag + cmass + area
						cmasses.append(cmass)
					if not os.path.exists(boundarydst):
						boundary = mask2boundary(mask)
						boundarymaster.append(boundary)
			if not os.path.exists(boundarydst):
				df = pd.DataFrame(boundarymaster)
				df.to_pickle(boundarydst)
			if not os.path.exists(cmassdst):
				df_cmass = pd.DataFrame(cmasses)
				df_cmass.columns = ['Filename','ImageID','ObjectID','X','Y','Area']
				df_cmass.index = df_cmass.index+1
				df_cmass.to_csv(os.path.join(setfolder,ch+'_object_ledger.csv'))
# getboundary('C:\\Users\\kuki\\Desktop\\cpoutput315\\Experiment1\\labeled image')

