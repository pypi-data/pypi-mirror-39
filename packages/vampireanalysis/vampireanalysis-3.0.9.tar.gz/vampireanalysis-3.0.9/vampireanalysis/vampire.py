#!/usr/bin/env python

# internal libraries
import os
# interface libraries
from Tkinter import *
from ttk import *
import tkFileDialog as fd
# my files
from main import main
from getboundary import getboundary
from list_set import list_set
from sum_binary import sum_binary

def makeform(root, fields):
	entries = {}
	rows= []
	for field in fields:
		row = Frame(root)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		if  field =='Merge CellProfiler Segmented Objects' or field == 'Create Object CSV' or field == 'Model' or field =='': 
			lab = Label(row, width=30, text=field, anchor='w',font=("Helvetica", 16))
			lab.pack(side=LEFT)
		else:
			ent = Entry(row)
			if field == 'Number of eigen-shapes':
				ent.insert(0,"choose a number")
			elif field == 'Status':
				ent.insert(0,'welcome to the vampire analysis')
			elif field == 'Model name':
				ent.insert(0,'name your model')
			elif field == 'Locate segmented images':
				ent.insert(0,'<--- click to load csv')
			else:ent.insert(0,"<--- click to search folder")
			ent.pack(side=RIGHT, expand=YES, fill=X)
			entries[field] = ent
			lab = Label(row, width=24, text=field+": ", anchor='w')
			lab.pack(side=LEFT)
		rows.append(row)
	return entries,rows

def getdir(entries,target):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'searching...')
	#################################################################
	folder = StringVar()
	foldername = fd.askdirectory()
	folder.set(foldername)
	folder = folder.get()
	entries[target].delete(0,END)
	entries[target].insert(0,folder)
	#################################################################
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'directory found...')

# def getcsv(entries,target):
# 	entries['Status'].delete(0,END)
# 	entries['Status'].insert(0,'searching...')
# 	#################################################################
# 	folder = StringVar()
# 	foldername = fd.askdirectory()
# 	folder.set(foldername)
# 	folder = folder.get()
# 	entries[target].delete(0,END)
# 	entries[target].insert(0,folder)
# 	#################################################################
# 	entries['Status'].delete(0,END)
# 	entries['Status'].insert(0,'directory found...')

def merge(entries,progress_bar,csvgen):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'merging...')
	progress_bar["maximum"] = 100
	#################################################################
	CPsubfolder = entries['Locate CellProfiler objects'].get() 
	# 'C:\\Users\\kuki\\Desktop\\cpoutput315\\Experiment1'
	labeledimfolder = os.path.join(CPsubfolder,'segmented images')
	if not os.path.isdir(labeledimfolder):
		os.mkdir(labeledimfolder)
		sum_binary(entries,CPsubfolder,progress_bar)
	#################################################################
	folder = os.path.join(CPsubfolder,'segmented images')
	if csvgen == True: list_set(folder)
	progress_bar["value"] = 100
	progress_bar.update()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'merging completed...')

def createobjectlist(entries,progress_bar):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'creating object csv...')
	progress_bar["maximum"] = 100
	#################################################################
	# input definition
	folder = entries['Locate segmented images'].get()
	# 'C:\\Users\\kuki\\Desktop\\cpoutput315\\Experiment1\\labeled image'
	# function
	getboundary(folder,progress_bar)
	#################################################################
	progress_bar["value"] = 100
	progress_bar.update()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'object csv created...')

def Model(entries,BuildModel,progress_bar):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'building model...')
	progress_bar["maximum"] = 100
	#################################################################
	# input definition
	clnum = entries['Number of eigen-shapes'].get()	#15
	folder = entries['Locate list of image sets'].get() #'C:\\Users\\kuki\\Desktop\\cpoutput315'
	modelname = entries['Model name'].get() #my model 1
	# function
	main(BuildModel,clnum,folder,entries,modelname,progress_bar)
	#################################################################
	progress_bar["value"] = 100
	progress_bar.update()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'modeling completed...')

def vampire(): 
	root = Tk()
	root.title("Vampire Analysis")
	fields = ('Merge CellProfiler Segmented Objects','Locate CellProfiler objects','',
		'Create Object CSV','Locate segmented images','',
		'Model','Locate list of image sets', 'Number of eigen-shapes','Model name','','Status')
	ents,rows = makeform(root, fields)
	root.bind('<Return>', (lambda event, e=ents: fetch(e))) 
	#####################################################################################################################
	#progress_bar
	progress_bar = Progressbar(rows[10], orient = 'horizontal',length=286, mode ='determinate')
	progress_bar.pack(side=LEFT,padx=5,pady=5)
	#####################################################################################################################
	#function 1 : merge
	b1 = Button(rows[1],text='search folder', width=12,command=(lambda e=ents: getdir(e,'Locate CellProfiler objects')))
	b1.pack(side=RIGHT,padx=5,pady=5)
	#function 2
	csvgen = BooleanVar()
	checkb = Checkbutton(rows[2],text='create list of image sets',variable=csvgen)
	b2 = Button(rows[2],text='merge', width=6,command=(lambda e=ents: merge(e,progress_bar,csvgen.get())))
	b2.pack(side=RIGHT,padx=5,pady=5)
	checkb.pack(side=RIGHT,padx=5,pady=5)
	#####################################################################################################################
	#function 3 : create csv
	b3 = Button(rows[4],text='load csv', width=12,command=(lambda e=ents: getdir(e,'Locate segmented images')))
	b3.pack(side=RIGHT,padx=5,pady=5)
	#function 4_1 : create image csv
	b4 = Button(rows[5],text='create',width=6,command=(lambda e=ents: createobjectlist(e,progress_bar)))
	b4.pack(side=RIGHT,padx=5,pady=5)
	#####################################################################################################################
	#function 5 : Model 
	b5 = Button(rows[7],text='search folder', width=12,command=(lambda e=ents: getdir(e,'Locate list of image sets')))
	b5.pack(side=RIGHT,padx=5,pady=5)
	#function 6
	b6 = Button(rows[10],text='apply model',width=12,command=(lambda e=ents: Model(e,False,progress_bar)))
	b6.pack(side=RIGHT,padx=5,pady=5)
	b7 = Button(rows[10],text='build model',width=12,command=(lambda e=ents: Model(e,True,progress_bar)))
	b7.pack(side=RIGHT,padx=5,pady=5)
	#####################################################################################################################
	#terminate
	quit = Button(root, text='Quit',width=6, command=root.quit)
	quit.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()
