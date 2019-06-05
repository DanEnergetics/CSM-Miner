"""CSMMiner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import shutil
import os
import json
import hashlib
import datetime
import backend
from xml.dom import minidom
from shutil import copyfile
from django.views.generic.base import RedirectView
from django.views.decorators.csrf import csrf_protect
from django.urls import path
from django.template import RequestContext, loader, Template, Context
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files import File
from django.contrib import admin
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django.conf.urls import include, url
from django.conf import settings
from django import template, forms


register = template.Library()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
snooping = HttpResponse("<body>Mr Moony presents his compliments to Professor Snape and begs him to keep his abnormally large nose out of other people's business. Mr Prongs agrees with Mr Moony and would like to add that Professor Snape is an ugly git. Mr Padfoot would like to register his astonishment that an idiot like that ever became a Professor. Mr Wormtail bids Professor Snape good day, and advises him to wash his hair, the slime-ball.</body>",content_type="text/html")

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def createProject(name):
	hashedName = hashlib.sha256(name.encode())
	hexed = hashedName.hexdigest()
	print(hexed)
	dir = os.path.join(BASE_DIR,'./Storage/',hexed)
	if not os.path.exists(dir):
		os.makedirs(dir)
		jsonContent = { 
			"name": name.replace('.xes',''),
			"filename": name,
			"creationTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"lastEdit": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"backgroundImgPath": "./images/matrix.png",
			"preProcessed": False
		}
		jsonConvert = json.dumps(jsonContent, indent=4, sort_keys=True)
		print(dir)
		fileW = open(os.path.join(dir ,"index.json"),"w")
		fileW.write(jsonConvert)
		fileW.close()
		return dir
	else:
		return "EXISTS"

def get_projects():
	result = []
	rt = ""
	workDir = BASE_DIR + "/Storage/"
	try:
		for d in os.listdir(workDir):
			if os.path.isdir(workDir + d) :
				with open(workDir + d + "/index.json") as json_file:
					result.append(json.load(json_file))
		rt = json.dumps(result)
		return rt
	except:
		print("Error.")

@register.filter
@csrf_protect
def get(request):
	context = {
		'projects': get_projects(),
	}
	return render(request, os.path.join(BASE_DIR,'./HTMLDocs/index.html'), context)


def request(rq,action):
	if not rq.method == 'GET':
		return HttpResponseNotFound("Error.")
	if action == "PROJECTS":
		return HttpResponse(get_projects(), content_type="application/json")
	elif action == "Dummy":
		return HttpResponse('{"viewCount" : 4}', content_type="application/json")
	try:
		jFile = file_get_contents(BASE_DIR + "/Storage/" + action + "/graph.json")
		return HttpResponse(jFile, content_type="application/json")
	except IOError:
		return snooping
	
@register.filter
@csrf_protect
def iframe(request,fileName):
	fileName += ".html"
	if request.method == 'POST':
		file = request.FILES.get('file',"EMPTY_REQ")
		if file == "EMPTY_REQ":
			context = {
				'msg' : "No file detected.",
			}
			return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)
		file = request.FILES['file']
		filename = file.name
		if not filename.endswith('.xes'):
			context = {
				'msg' : "Wrong format detected.",
			}
			return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)
		md = File(file)
		DEST_DIR = createProject(filename)
		if not DEST_DIR == "EXISTS":
			context = {
				'msg' : "FILE_OK",
			}
			with open(os.path.join(DEST_DIR,filename),'wb+') as dest:
				for chunk in md.chunks():
					dest.write(chunk)
			backend.BackEnd.call()
			return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)
		context = {
			'msg' : "Project already exists."
		}
		return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)
	context = {
		'msg' : "",
	}
	return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)	


def getImg(request,fileName):
	try:
		with open(BASE_DIR + "/HTMLDocs/images/" + fileName + ".png", "rb") as f:
			return HttpResponse(f.read(), content_type="image/jpeg")
	except IOError:
		return snooping

def getSVG(request,fileName):
	try:
		with open(BASE_DIR + "/HTMLDocs/images/" + fileName + ".svg", "rb") as f:
			return HttpResponse(f.read(), content_type="image/svg+xml")
	except IOError:
			return snooping

		
def getJs(request,fileName):
	try:
		with open(BASE_DIR + "/HTMLDocs/ext/" + fileName + ".js") as js:
			return HttpResponse(js.read(), content_type="application/x-javascript")
	except IOError:
		return snooping

def getText(request,fileName):
	try:
		content = file_get_contents(BASE_DIR + "/HTMLDocs/ext/res/" + fileName + ".txt")
		return HttpResponse(content, content_type="text")
	except IOError:
		return snooping
	
def getCSS(request):
	try:
		content = file_get_contents(BASE_DIR + "/HTMLDocs/ext/css/common.css")
		return HttpResponse(content, content_type="text/css")
	except IOError:
		return snooping
	
def getMani(request):
	try:
		content = file_get_contents(BASE_DIR + "/HTMLDocs/images/manifest.json")
		return HttpResponse(content, content_type="application/json")
	except IOError:
		return snooping
def rm(r,project):
	if project != "Dummy":
		name = project + ".xes"
		hashedName = hashlib.sha256(name.encode())
		hexed = hashedName.hexdigest()
		print(hexed)
		dir = os.path.join(BASE_DIR,'./Storage/',hexed)	
		shutil.rmtree(dir,True)
		return HttpResponse("OK")

def getSampleJson(r):
	jsonF = file_get_contents(BASE_DIR + "/HTMLDocs/sample.json")
	return HttpResponse(jsonF,content_type="application/json")

CU = {
	'UID' : '99adc231b045331e514a516b4b7680f588e3823213abe901738bc3ad67b2f6fcb3c64efb93d18002588d3ccc1a49efbae1ce20cb43df36b38651f11fa75678e8',
}

def createUID(r):
	ip = r.META.get('REMOTE_ADDR')
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	UID = hashlib.sha512((ip+time).encode('utf-8'))
	CU.update({UID})
	return HttpResponse(UID)

def removeUID(UID):
	print("Not implemented.")

def sock(req,UID):
	if not UID in CU:
		return HttpResponse("Error. No open connection.")
	if not req.method == 'POST':
		return HttpResponse("Error. No request fonud.")
	json_req = json.loads(req.body)
	try:
		req_data = json_req['data']
	except KeyError:
		HttpResponse("Error. Malformed data.")
	parsed_req = req_data['sock']
	response = {}
	for entry in parsed_req:
		print(entry)
	return HttpResponse(json.dumps(response))

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', get),
	path('<slug:fileName>.js', getJs, name="fileName"),
	path('images/<slug:fileName>.png', getImg, name="fileName"),
	path('<slug:fileName>.svg', getSVG, name="fileName"),
	path('<slug:fileName>.html', iframe, name="fileName"),
	path('request/rm/<slug:project>.xes', rm, name="project"),
	path('request/<slug:action>.json', request , name='action'),
	#The following patterns are exclusively used by mxClient, therefor ONLY mxClient resources should be stored in the corresponding paths.
	path('resources/<slug:fileName>.txt', getText, name="fileName"),
	path('css/common.css',getCSS),
	#Favicon links
	path('manifest.json',getMani),
	path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
	#sample json
	path('sample.json',getSampleJson),
	#Socket communication
	path('Socket/open.connection', createUID),
	path('Socket/<slug:UID>', sock, name="UID"),
]
