#!/usr/bin/env python

# built-in libraries
import os
import pickle
import random
from time import sleep
# external libraries
import pandas as pd
import numpy as np
# my wrapper
from collect_selected_bstack import *
from recordIDX import *
# my core
from bdreg import *
from pca_bdreg import *
from clusterSM import *

# def main(buildmodel,clnum,folder,entries,modelname,progress_bar=None):
def main(BuildModel,clnum,folder,entries,modelname,progress_bar=None):
	print('## main.py')
	if BuildModel:
		cell,nuc = collect_seleced_bstack(folder,BuildModel)

		VamModel = {
		"N":[],
		"bdrn":[],
		"mdd":[],
		"sdd":[],
		"pc":[],
		"latent":[],
		"clnum":[],
		"pcnum":[],
		"mincms":[],
		"testmean":[],
		"teststd":[],
		"boxcoxlambda":[],
		"C":[],
		"dendidx":[]
		}
		N = None

		cellornuc = 'cells'
		progress_bar["value"] = 10
		progress_bar.update()
		bdpc, bnreg, sc, VamModel = bdreg_main(cell,N,VamModel,BuildModel)
		progress_bar["value"] = 20
		progress_bar.update()
		pc , score, latent, VamModel = pca_bdreg_main(bdpc,VamModel,BuildModel)
		progress_bar["value"] = 30
		progress_bar.update()
		pcnum=None
		IDX,bdsubtype,C,VamModel = cluster_main(folder,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel,cellornuc)
		progress_bar["value"] = 40
		progress_bar.update()
		if not os.path.exists(os.path.join(folder,'picklejar')):
			os.mkdir(os.path.join(folder,'picklejar'))
		if os.path.exists(os.path.join(os.path.join(folder,'picklejar'),modelname+'_cells.pickle')):
			f=open(os.path.join(os.path.join(folder,'picklejar'),modelname + str(random.randint(0,100)) +'_cell.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		else:
			f=open(os.path.join(os.path.join(folder,'picklejar'),modelname+'_cells.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		progress_bar["value"] = 45
		progress_bar.update()
		result = recordIDX(IDX,BuildModel,folder,cellornuc)
		progress_bar["value"] = 50
		progress_bar.update() 

		cellornuc = 'nuclei'
		progress_bar["value"] = 55
		progress_bar.update()
		bdpc, bnreg, sc, VamModel = bdreg_main(nuc,N,VamModel,BuildModel)
		progress_bar["value"] = 60
		progress_bar.update()
		pc , score, latent, VamModel = pca_bdreg_main(bdpc,VamModel,BuildModel)
		progress_bar["value"] = 70
		progress_bar.update()
		pcnum=None
		IDX,bdsubtype,C,VamModel = cluster_main(folder,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel,cellornuc)
		progress_bar["value"] = 80
		progress_bar.update()

		if os.path.exists(os.path.join(os.path.join(folder,'picklejar'),modelname+'_nuclei.pickle')):
			f=open(os.path.join(os.path.join(folder,'picklejar'),modelname + str(random.randint(0,100)) +'_nuclei.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		else:
			f=open(os.path.join(os.path.join(folder,'picklejar'),modelname+'_nuclei.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()

		progress_bar["value"] = 90
		progress_bar.update()

		result = recordIDX(IDX,BuildModel,folder,cellornuc)
		progress_bar["value"] = 95
		progress_bar.update() 

	else:
		cell,nuc = collect_seleced_bstack(folder,BuildModel)
		progress_bar["value"] = 10
		progress_bar.update()

		try:
			f=open(os.path.join(os.path.join(folder,'picklejar'), modelname +'_cells.pickle'),'r')
		except:
			entries['Status'].delete(0,END)
			entries['Status'].insert(0,'the model does not exist. please replace model name to the one you built')
		VamModel = pickle.load(f)

		N = VamModel['N'] 
		cellornuc = 'cells'

		progress_bar["value"] = 20
		progress_bar.update()
		bdpc_new, bnreg_new, sc_new, VamModel = bdreg_main(cell,N,VamModel,BuildModel)
		progress_bar["value"] = 30
		progress_bar.update()
		pc_new, score_new, latent_new, VamModel = pca_bdreg_main(bdpc_new,VamModel,BuildModel)
		progress_bar["value"] = 40
		progress_bar.update()
		clnum=VamModel['clnum']
		pcnum=VamModel['pcnum']
		#pc_new goes in for sake of placing, but pc from the model is used in cluster_main
		IDX_new,bdsubtype_new,C_new,VamModel = cluster_main(folder,modelname,score_new,pc_new,bdpc_new,clnum,pcnum,VamModel,BuildModel,cellornuc)
		progress_bar["value"] = 50
		progress_bar.update()

		result = recordIDX(IDX_new,BuildModel,folder,cellornuc)

		try:
			f=open(os.path.join(os.path.join(folder,'picklejar'), modelname +'_nuclei.pickle'),'r')
		except:
			print('error')
			# entries['Status'].delete(0,END)
			# entries['Status'].insert(0,'the model does not exist. please replace model name to the one you built')
		VamModel = pickle.load(f)

		N = VamModel['N'] 
		cellornuc = 'nuclei'
		progress_bar["value"] = 60
		progress_bar.update()
		bdpc_new, bnreg_new, sc_new, VamModel = bdreg_main(nuc,N,VamModel,BuildModel)
		progress_bar["value"] = 70
		progress_bar.update()
		pc_new, score_new, latent_new, VamModel = pca_bdreg_main(bdpc_new,VamModel,BuildModel)
		progress_bar["value"] = 80
		progress_bar.update()
		clnum=VamModel['clnum']
		pcnum=VamModel['pcnum']
		#pc_new goes in for sake of placing, but pc from the model is used in cluster_main
		IDX_new,bdsubtype_new,C_new,VamModel = cluster_main(folder,modelname,score_new,pc_new,bdpc_new,clnum,pcnum,VamModel,BuildModel,cellornuc)
		progress_bar["value"] = 90
		progress_bar.update()

		result = recordIDX(IDX_new,BuildModel,folder,cellornuc)

		# entries['Status'].delete(0,END)
		# entries['Status'].insert(0,'applied the model')


# BuildModel = False
# clnum = 15
# folder = 'C:\\Users\\kuki\\Desktop\\cpoutput315'
# modelname = 'testtest'
# main(BuildModel,clnum,folder,modelname)