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
from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader, Template, Context
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.core.files import File
from django.http import HttpResponseNotFound
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django import template
from xml.dom import minidom
import hashlib
import json
from shutil import copyfile

register = template.Library()

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

register = template.Library()

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
		jsonContent = '{ "name":"' + name +'", "filename":"' + name + '", "creationTime":"' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'", "lastEdit":"' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'", "backgroundImgPath": "' + BASE_DIR +'/HTMLDocs/images/matrix.png", "preProcessed": "NO",}'
		jsonConvert = json.dumps(jsonContent, indent=4, sort_keys=True)
		print(dir)
		fileW = open(os.path.join(dir ,"index.json"),"w")
		fileW.write(jsonConvert)
		fileW.close()
		return dir
	else:
		return "EXISTS"

def get_projects():
	return {'project1','project2'}
def get_id():
	return 1

@csrf_protect
def get(request):
	context = {
		'projects': get_projects(),
		'id' : get_id(),
	}
	return render(request, os.path.join(BASE_DIR,'./HTMLDocs/index.html'), context)


def request(rq,action):
	if not rq.method == 'GET':
		return HttpResponseNotFound("Error.")
	print(action)
	"""
	TO-DO : #IMPLEMENT THE QUEUE ROUTINE
	"""
	return HttpResponse('<body>OK</body>')
	
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
			return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)
		context = {
			'msg' : "Project already exists."
		}
		return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)
	context = {
		'msg' : "",
	}
	return render(request, os.path.join(BASE_DIR,"HTMLDocs/",fileName), context)	


def mainHandle(request,string):
	handleForm(request)
	return main(request)
	
urlpatterns = [
    path('admin/', admin.site.urls),
	path('', get),
	path('<slug:fileName>.html', iframe, name="fileName"),
	path('request/<slug:action>', request , name='action'),
]
