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

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

register = template.Library()

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

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
	
@csrf_protect
def iframe(request,file):
	if request.method == 'POST':
		file = request.FILES.get('file',"EMPTY_REQ")
		if file == "EMPTY_REQ":
			context = {
				'msg' : "No file
				 detected.",
			}
			return render(request, os.path.join(BASE_DIR,'./HTMLDocs/index.html'), context)
		file = request.FILES['file']
		filename = file.name
		if not filename.endswith('.xes'):
			context = {
				'msg' : "Wrong format detected.",
			}
			return render(request, os.path.join(BASE_DIR,'./HTMLDocs/',file,'.html'), context)
		md = File(file)
		with open(os.path.join(BASE_DIR,'./Storage/',filename),'wb+') as dest:
			for chunk in md.chunks():
				dest.write(chunk)
	


def mainHandle(request,string):
	handleForm(request)
	return main(request)
	
urlpatterns = [
    path('admin/', admin.site.urls),
	path('', get),
	path('/<slug:fileName>.html', iframe, name="fileName"),
	path('request/<slug:action>', request , name='action'),
]
