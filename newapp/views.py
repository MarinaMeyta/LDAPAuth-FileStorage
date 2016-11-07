import os
import mimetypes
from django.shortcuts import render
#from ldap3 import Server, Connection, ALL
from django.conf import settings
from .forms import UploadFileForm
from django.http import HttpResponseRedirect, HttpResponse

from .auth import LDAPBackend

from django.contrib import messages


def login_page(request):
    return render(request, 'login.html', {})


def upload_file_page(request):
    return render(request, 'upload_file.html', {})

def success(request):
    return render(request, 'success.html', {})


def login(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        print('USERNAME==========', username)
        password = request.POST.get('password')
        print('PASSWORD==========', password) 

        user = LDAPBackend.authenticate(username, password)
        if user:            
            return HttpResponseRedirect('/upload_file/')
    return render(request, 'login.html', {})


def upload_file(request):
    print('request.session.get(username): ',request.session.get('username'))
    
    if request.method == 'POST': 
        form = UploadFileForm(request.POST, request.FILES)     
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], request.FILES['file'].name)
            return HttpResponseRedirect('/success/')
    else:
        form = UploadFileForm()
        files = os.listdir(settings.ACTIVE_DIRECTORY_FILES)
    if request.method == 'GET':
        path = '/download/' + os.path.basename(request.path)
        print(path)
        if os.path.basename(request.path):
            return HttpResponseRedirect(path)
    return render(request, 'upload_file.html', {'form':form, 'files':files})       
 
    
    
def handle_uploaded_file(f, t):
    with open(settings.ACTIVE_DIRECTORY_FILES + '\\' + t, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        
        
def send_file(request):
    filename = os.path.basename(request.path)
    filepath = settings.ACTIVE_DIRECTORY_FILES + '\\' + filename
    
    if filename:
        content_type = mimetypes.guess_type(filename)[0]
        f = open(filepath, 'rb')
        response = HttpResponse(f, content_type=content_type)
        response['Content-Length'] = os.path.getsize(filepath)    
        response['Content-Disposition'] = 'attachment; filename=%s'%filename
        return response
    return render 
