# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from .view_models import HelperViewModel, ProjectViewModel, InternalProjectViewModel

from com.vsa.file_handler.file_handler import File_Handler
from com.vsa.utilities.directories import Directory

def index(request):
    return render(request,"CodeClone/index.html")

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request,"CodeClone/dashboard.html")

def contact_us(request):
    if request.method == 'POST':
        return render(request, "CodeClone/contact_us.html")
    model = {0: [1, 2, 3, 4] , 1:[5, 6, 7, 8]}
    viewModel = {"model":model}
    return render(request, "CodeClone/contact_us.html", viewModel)

def projects(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        project_lang = request.POST['project_language']
        username = request.session['username']

        if Directory.is_exist_dir("projects/"+username+"/"+project_name):
            messages.error(request, 'Project Already Exist Make another project !')
            return redirect('projects')

        dirs = Directory.get_directory_of("projects/"+username+"/"+project_name)
        request.session['dir_dataset'] = username+"/"+project_name
        request.session['dir_project'] = dirs
        #print(Directory.make_dir(dirs))
        #print(request.session['dir_dataset'])
        #print(request.session['dir_project'])
        return redirect("project-features")

    dirs = Directory.get_directory_of("projects/"+request.session['username'])
    projects = Directory.get_all_folders(dirs)
    return render(request, "CodeClone/projects.html", {"projects": projects})

def project_features(request, project_name=None):
    model = ProjectViewModel()
    if project_name is not None:
        print("PROJECT IS HERE")
        print(project_name)
        username = request.session['username']
        dirs = Directory.get_directory_of("projects/"+username+"/"+project_name)
        request.session['dir_dataset'] = username+"/"+project_name
        request.session['dir_project'] = dirs

    if request.method == 'POST':

        Directory.delete_dir('com/vsa/datasets/'+request.session['dir_dataset'])
        Directory.delete_dir(request.session['dir_project'])

        for afile in request.FILES.getlist('project1'):
            if HelperViewModel.is_file_java(str(afile)):
                #File_Handler.write_file(afile, 'Users/'+str(request.session['username'])+'/projects/project1')
                File_Handler.write_file(afile, str(request.session['dir_project'])+'project1')
        for afile in request.FILES.getlist('project2'):
            if HelperViewModel.is_file_java(str(afile)):
                #File_Handler.write_file(afile, 'Users/'+str(request.session['username'])+'/projects/project2')
                File_Handler.write_file(afile, str(request.session['dir_project'])+'project2')

        dirs = [Directory.get_directory_of(str(request.session['dir_project'])+'project1'),
                Directory.get_directory_of(str(request.session['dir_project'])+'project2')]

        nGram = request.POST['nGramRange']

        res = model.run_test_Project(username=str(request.session['dir_dataset']), dirs=dirs, ngram=int(nGram))
        #print(res)
        view_model = {'model': model}
        return render(request, "CodeClone/project_features.html", view_model)

    return render(request, "CodeClone/project_features.html")

def internal_projects(request):
    if request.method == 'GET':
        dirs = Directory.get_directory_of("projects/" + request.session['username'])
        projects = Directory.get_all_folders(dirs)
        return render(request, "CodeClone/internal_projects.html", {"projects": projects})
    return render(request, "CodeClone/internal_projects.html")

def internal_features(request, project_name=None):
    model = InternalProjectViewModel()
    if project_name is not None:
        print("PROJECT IS HERE")
        print(project_name)
        username = request.session['username']
        dirs = Directory.get_directory_of("projects/"+username+"/"+project_name)
        request.session['dir_dataset'] = username+"/"+project_name
        request.session['dir_project'] = dirs

    if request.method == "POST":
        try:
            if 'project1_features' in request.POST:
                res = model.run_test_Project(username=str(request.session['dir_dataset']), project_no=1)
                view_model = {'model': model}
                return render(request, "CodeClone/internal_features.html", view_model)
            if 'project2_features' in request.POST:
                res = model.run_test_Project(username=str(request.session['dir_dataset']), project_no=2)
                view_model = {'model': model}
                return render(request, "CodeClone/internal_features.html", view_model)

        except Exception as e:
            print(e)
            raise Http404(e.__str__())

    return render(request, "CodeClone/internal_features.html")

def delete_project(request, project_name):
    username = request.session['username']
    Directory.delete_dir('com/vsa/datasets/' + username+"/"+project_name)
    Directory.delete_dir("projects/"+username+"/"+project_name)
    return redirect('projects')

def reg(request):
    form = UserForm
    return render(request, "Accounts/registration_form.html", {'form': form})

def log(request):
    return render(request, "Accounts/login_form.html")


