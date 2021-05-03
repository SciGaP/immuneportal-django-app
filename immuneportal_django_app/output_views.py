##IMPORTS FOR LOGOS START######################
import pandas
from collections import OrderedDict
from collections import Counter
import numpy
import matplotlib.pyplot as plt
import logomaker
import io


##IMPORTS FOR LOGOS ENDING####################



import io
import os


import numpy as np
#import pandas


from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from urllib.parse import quote
from django.urls import reverse
from django.template.loader import render_to_string

#getting files loaded
#from airavata_django_portal_sdk import user_storage

from airavata_django_portal_sdk import urls
#urls.get_download_url()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SplicePredLink:
	display_type = "link"
	immediate = True
	name = "Splicing File"

	def generate_data(self, request, experiment_output, experiment, output_file=None):
		return {
			"label": "Analyze in MapTool",
			"url": "www.google.com",
		}
		
		
class SplicePredTable:
	display_type = 'html'
	name = 'Splicing Table'
	# Optionally provide path to a file to test with when data isn't available
	# locally
	# fixture_output_file = ""

	def generate_data(self, request, experiment_output, experiment, output_file=None):
		link = urls.get_download_url(experiment_output.value)
		print("FILE URL",link)
		return {
			'output': render_to_string(
				
				'immuneportal_django_app/splicetable.html', {'outputFilePath' : link}),
			'js':"/static/js/datatable.js"
			}
			
class IrneoPredLink:

	display_type = "link"
	immediate = True
	name = "ImmunePortal Output"
	
	#print("FILE URL",link)
	def generate_data(self, request, experiment_output, experiment, output_file=None):
	
			
		link = urls.get_download_url(experiment_output.value)
		return {
			"label": "Output Visualization",
			"url": "https://immuneportal.ccbb.iupui.edu/immuneportal_django_app/expviz/?=https://immuneportal.ccbb.iupui.edu"+link,
		}
		
	
			
			
class SplicePlot:
	display_type = 'image'
	name = "SplicePlot"
	def generate_data(self, request, experiment_output, experiment, output_file=None):
		#print('THIS IS MY TYPE',type(experiment_output.value))
		#print('value',experiment_output.value)
		#print('directory',os.getcwd())
		#df=pandas.read_csv(output_file)
		#print('HEY THERE IM HERE',df.columns)
		
		#plt.plot([0,1,2],[1,1.25,1.7])

		# Export plot as image buffer
		#buffer = io.BytesIO()
		#plt.savefig(buffer, format='png')
		#image_bytes = buffer.getvalue()
		#buffer.close()

		# return dictionary with image data
		return {
			'image': image_bytes,
			'mime-type': 'image/png'
		}
		
class irneoSeq:
	display_type = 'image'
	name = "SeqLogo"
	def generate_data(self, request, experiment_output, experiment,output_file=None):
		#print('output_file type',type(output_file))
		#print('value',experiment_output.value)
		#link = urls.get_download_url(experiment_output.value)
		#print("FILE URL",link)
		#print('directory',os.getcwd())
		dfTest=pandas.read_json(output_file.read().decode())
		#print(dfTest.head())
		#print('contents',os.listdir('django_airavata/static'))
		
		#os.system('wget localhost:8000/api/download?data-product-uri=airavata-dp%3A%2F%2Fa4d1e8cf-3879-469e-b391-bac0d953f72e')
		
		#df=pandas.read_csv('/code/django_airavata/static/files/test_Aligned.sortedByCoord.out_intron_candidates_weak_bind_peptide_predict_result.txt',delimiter='\t')



		mut_pep=df['mut_pep']

		maxlen=max([len(pep) for pep in mut_pep])
		#print(maxlen)

		#need list for given position(11 total)
		listOfPosLists=[]
		for pos in range(maxlen):
			posList=[]
			for pep in mut_pep:
				if pos<=len(pep)-1:
					posList.append(pep[pos])
			#else:
			#	posList.append('')
			listOfPosLists.append(posList)

		#TAKES INTO ACCOUNT OVERHANG ON RIGHT with '', so must consider '' for all positions 
		aminos=['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']

		freqLists=[]
		for l in listOfPosLists:
			countDict=dict(Counter(l))
			#print(countDict)
			for a in aminos:
				if a not in countDict:
					countDict[a]=0
			freqLists.append([x[1]/len(l) for x in sorted(countDict.items())])

		#print(sum([x[1]/len(mut_pep) for x in freqLists[6]]))


		#print(numpy.asarray(freqLists))

		pwm=numpy.asarray(freqLists)

		renderDf = pandas.DataFrame(pwm, columns = sorted(aminos))

		logomaker.Logo(renderDf)

		#print(htype)
		
		buffer = io.BytesIO()
		plt.savefig(buffer, format='png')
		image_bytes = buffer.getvalue()
		buffer.close()
		return {
			'image': image_bytes,
			'mime-type': 'image/png'
		}
		



