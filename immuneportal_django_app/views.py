from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
import pandas as pd
from collections import Counter
import os
import pandas
import numpy
from upsetplot import generate_counts
from upsetplot import plot
import matplotlib.pyplot as plt
import logomaker
import requests
import io
import seaborn as sns
from subprocess import check_output
from io import StringIO
from airavata_django_portal_sdk import user_storage
import base64
from collections import Counter
from airavata_django_portal_sdk import urls
import time
import json
#from airavata_django_portal_sdk import urls




@login_required
def image_view(request):
	requestStr=str(request)
	print("THIS IS THE REQUEST",requestStr)
	
	data_product_uri=request.GET['data-product-uri']
	#print(request)
	#requestStr=requestStr.replace("<WSGIRequest: GET '","")
	#requestStr=requestStr.replace("'>","")
	#requestStr=requestStr.split('=')[2]
	#print("THIS IS THE REQUEST",requestStr)
	#request='/api'+request
	#print("THIS IS THE REQUEST",requestStr)
	#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
	#df=pandas.read_csv("http://localhost:8000"+request, delimiter='\t')

	#url="http://localhost:8000"+request
	
	#data_product = request.airavata_client.getDataProduct(request.authz_token, data_product_uri)
	data_product = user_storage.open_file(request, data_product_uri=data_product_uri)
	
	#data_product=request.airavata_client.getDataProduct(request.authz_token, data_product_uri)
	#s=requests.get(url, headers= headers).text
	
	#print(s)
	df=pandas.read_csv(data_product, sep="\t")
	print(df.head())
	
	#df=pandas.read_csv(output_file, delimiter='\t')
	mut_pep=df['mut_pep']
	maxlen=max([len(pep) for pep in mut_pep])
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
	pwm=numpy.asarray(freqLists)
	renderDf = pandas.DataFrame(pwm, columns = sorted(aminos))
	logomaker.Logo(renderDf)
	buffer = io.BytesIO()
	plt.savefig(buffer, format='png')
	image_bytes = buffer.getvalue()
	image_bytes=base64.b64encode(image_bytes)
	buffer.close()
	
	return HttpResponse(image_bytes, content_type="image/png")
	



@login_required
def expviz(request):
	return render(request, "immuneportal_django_app/expviz.html")
	
@login_required
def splice_res(request):
	return render(request, "immuneportal_django_app/splicetable.html")



@login_required
def languages(request):
	return JsonResponse({'languages': [{
		'lang': 'French',
		'greeting': 'bonjour',
	}, {
		'lang': 'German',
		'greeting': 'guten tag'
	}, {
		'lang': 'Hindi',
		'greeting': 'namaste'
	}, {
		'lang': 'Japanese', 
		'greeting': 'konnichiwa'
	}, {
		'lang': 'Swahili',
		'greeting': 'jambo'
	}, {
		'lang': 'Turkish', 
		'greeting': 'merhaba'
	}]})
