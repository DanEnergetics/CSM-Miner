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
import datetime
import os
from django.shortcuts import render
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django import template, forms
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader, Template, Context
from django.views.decorators.csrf import csrf_protect
from django.core.files import File
from django.http import HttpResponseNotFound
from django.conf.urls import (handler400, handler403, handler404, handler500)
from xml.dom import minidom
import hashlib
import json
from shutil import copyfile
from django.conf import settings
from django.views.generic.base import RedirectView
import backend

register = template.Library()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
	try:
		jFile = file_get_contents(BASE_DIR + "/Storage/" + action + "/graph.json")
		return HttpResponse(jFile, content_type="application/json")
	except IOError:
		return HttpResponseNotFound("404")
	
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
		red = Image.new('RGBA', (1, 1), (255,0,0,0))
		response = HttpResponse(content_type="image/jpeg")
		red.save(response, "JPEG")
		return response
		
def getSVG(request,fileName):
	try:
		with open(BASE_DIR + "/HTMLDocs/images/" + fileName + ".svg", "rb") as f:
			return HttpResponse(f.read(), content_type="image/svg+xml")
	except IOError:
		red = Image.new('RGBA', (1, 1), (255,0,0,0))
		response = HttpResponse(content_type="image/svg+xml")
		red.save(response, "JPEG")
		return response
		
def getJs(request,fileName):
	try:
		with open(BASE_DIR + "/HTMLDocs/ext/" + fileName + ".js") as js:
			return HttpResponse(js.read(), content_type="application/x-javascript")
	except IOError:
		return HttpResponse("<body>ERROR.</body>")

def getText(request,fileName):
	try:
		content = file_get_contents(BASE_DIR + "/HTMLDocs/ext/res/" + fileName + ".txt")
		return HttpResponse(content, content_type="text")
	except IOError:
		return HttpResponse("<body>ERROR.</body>")
	
def getCSS(request):
	try:
		content = file_get_contents(BASE_DIR + "/HTMLDocs/ext/css/common.css")
		return HttpResponse(content, content_type="text/css")
	except IOError:
		return HttpResponse("<body>ERROR.</body>")
	
def getMani(request):
	try:
		content = file_get_contents(BASE_DIR + "/HTMLDocs/images/manifest.json")
		return HttpResponse(content, content_type="application/json")
	except IOError:
		return HttpResponse("<body>ERROR.</body>")
	

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', get),
	path('<slug:fileName>.js', getJs, name="fileName"),
	path('images/<slug:fileName>.png', getImg, name="fileName"),
	path('<slug:fileName>.svg', getSVG, name="fileName"),
	path('<slug:fileName>.html', iframe, name="fileName"),
	path('request/<slug:action>.json', request , name='action'),
	#The following patterns are exclusively used by mxClient, therefor ONLY mxClient resources should be stored in the corresponding paths.
	path('resources/<slug:fileName>.txt', getText, name="fileName"),
	path('css/common.css',getCSS),
	#Favicon links
	path('manifest.json',getMani),
	path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
]
