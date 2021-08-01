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
#import seaborn as sns
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
def upset_view(request):
	currkey=None
	for key in list(request.GET.keys()):
		print(key)
		if 'airavata-dp' in key:
			currkey=key
			
			#currkey=key.replace("thisuri,","");
			print(currkey)
	#if 'upset' in list(request.GET.keys()):
	#print('UPSET VIEW CURRENT DIRECTORY',os.getcwd())
	fdata=user_storage.open_file(request, data_product=None, data_product_uri=currkey)
	d1=pd.read_csv(fdata,header=0,sep="\t")
	print('SUPPOSED SUCCESS')
	hla_cols = [col for col in d1.columns if 'HLA-' in col]
	d2= d1[hla_cols]
	dlist= d2.values.tolist()


	upset_list=[]

	for item in dlist:
		indexs= [ n for n,i in enumerate(item) if i<2 ]
		hlagroups= ','.join([ hla_cols[j] for j in indexs])
		upset_list.append(hlagroups)

	sumList= [ hla_cols + ['count'] ]
	cc= Counter(upset_list)
	for key, value in cc.items():
		hlaS= key.split(',')
		ToF=[]
		for m in hla_cols:
			if m in hlaS:
				ToF.append(True)
			else:
				ToF.append(False)
		
		sumList.append(ToF + [value])

	upSet= pd.DataFrame(sumList[1:],columns=sumList[0]);
	print(upSet) #### here for the right panel data
	counts=upSet['count']
	upSet = upSet.drop(labels='count', axis=1)

	#INITIALIZE TUPLE INDEX TO GET RID OF DUPLICATES
	tupList=[]
	for idx, row in upSet.iterrows():

		tupList.append(tuple(row))
	index = pd.MultiIndex.from_tuples(tupList, names=list(upSet.columns))
	upsetData=pd.Series(numpy.array(list(counts)), index=index)
	
	plot(upsetData)

	
	buffer = io.BytesIO()
	plt.savefig(buffer, format='png')
	image_bytes2 = buffer.getvalue()
	#savedFile1=user_storage.save(request,'.',image_bytes2,name='upset', content_type=None, storage_resource_id=None)
	#print("SAVED FILE",savedFile1)
	image_bytes2=base64.b64encode(image_bytes2)
	buffer.close()
	#time.sleep(1)
	
	
	return HttpResponse(image_bytes2, content_type="image/png")
	
	

@login_required
def hlaload_view(request):
	print("THESE KEYS",request.GET.keys())
	
	
	currkey=None
	for key in list(request.GET.keys()):
		print(key)
		if 'airavata-dp' in key:
			currkey=key
			
			#currkey=key.replace("thisuri,","");
			print(currkey)
	#if 'upset' in list(request.GET.keys()):
	#print('UPSET VIEW CURRENT DIRECTORY',os.getcwd())
	fdata=user_storage.open_file(request, data_product=None, data_product_uri=currkey)
	
	print('SUPPOSED SUCCESS')
	
	d1=pd.read_csv(fdata,header=0,sep="\t")
	individual=len(d1)
	#individual=int(str(check_output(["wc","-l","django_airavata/static/files/Immunoportal_data.txt"]).decode("utf-8")).split(' ')[0])
	#tcga=pandas.read_csv('TCGA_IRneoAg_load_in_8cancers_summary.csv')

	#tcga=tcga[tcga['canType']=='BRCA']
	#print(tcga)

	#alpha, loc , beta=5,100,22
	#data=ss.gamma.rvs(alpha,loc=loc,scale=beta,size=5000)

	plt.axvline(individual, color='red')

	#ax=sns.kdeplot(tcga['weakBinder'])
	plt.xlabel("Intron Neoantigen Load")

	buffer = io.BytesIO()
	
	#savedFile=user_storage.save(request,'.',image_bytes,name=None, content_type=None, storage_resource_id=None)
	
	plt.savefig(buffer, format='png')
	image_bytes = buffer.getvalue()
	#savedFile2=user_storage.save(request,'.',image_bytes,name=None, content_type=None, storage_resource_id=None)
	#print("SAVED FILE",savedFile2)
	image_bytes=base64.b64encode(image_bytes)
	buffer.close()
	#time.sleep(1)
	
	return HttpResponse(image_bytes, content_type="image/png")
	
@login_required
def delete(request):
	print("THESE KEYS",request.GET.keys())
	
	
	currkey=None
	for key in list(request.GET.keys()):
		print(key)
		if 'airavata-dp' in key:
			currkey=key
			
			#currkey=key.replace("thisuri,","");
			print(currkey)
	user_storage.delete(request,data_product=None, data_product_uri=currkey)
	
	return HttpResponse('deleted', content_type="text/html")


@login_required
def expviz(request):
	return render(request, "immuneportal_django_app/expviz.html")

@login_required
def splice_res(request):
	return render(request, "immuneportal_django_app/splicetable.html")

'''

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
	
'''
