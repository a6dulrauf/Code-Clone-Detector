# Create your views here.
import json

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
from com.vsa.elements import languages

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
        HelperViewModel.set_project_language(dirs, project_lang)
        request.session['dir_dataset'] = username+"/"+project_name
        request.session['dir_project'] = dirs
        return redirect("project-features")

    dirs = Directory.get_directory_of("projects/"+request.session['username'])
    projects = Directory.get_all_folders(dirs)
    return render(request, "CodeClone/projects.html",
                  {"projects": projects, "language_options": languages.options()})

def project_features(request, project_name=None):
    model = ProjectViewModel()
    if project_name is not None:
        username = request.session['username']
        dirs = Directory.get_directory_of("projects/"+username+"/"+project_name)
        request.session['dir_dataset'] = username+"/"+project_name
        request.session['dir_project'] = dirs

    # Language of the currently-open project (from its marker; default java).
    project_dir = str(request.session.get('dir_project', ''))
    language = HelperViewModel.get_project_language(project_dir) if project_dir else languages.DEFAULT
    exts = languages.get(language).extensions
    lang_ctx = {'language': language, 'accept': ','.join(exts)}

    if request.method == 'POST':
        if 'dir_project' not in request.session or 'dir_dataset' not in request.session:
            messages.error(request, 'Open a project first, then run the comparison.')
            return redirect('projects')

        # A folder picker sends every file it finds; keep only this language's.
        p1_uploads = [f for f in request.FILES.getlist('project1') if HelperViewModel.is_supported_file(str(f), language)]
        p2_uploads = [f for f in request.FILES.getlist('project2') if HelperViewModel.is_supported_file(str(f), language)]

        # Replace a slot ONLY when fresh source files arrived for it. Never wipe
        # the whole project up front: that used to destroy the other slot and
        # the seeded demo whenever an upload contained no source files.
        if p1_uploads:
            Directory.delete_dir(project_dir + 'project1')
            for afile in p1_uploads:
                File_Handler.write_file(afile, project_dir + 'project1')
        if p2_uploads:
            Directory.delete_dir(project_dir + 'project2')
            for afile in p2_uploads:
                File_Handler.write_file(afile, project_dir + 'project2')

        dirs = [Directory.get_directory_of(project_dir + 'project1'),
                Directory.get_directory_of(project_dir + 'project2')]

        # Validate before running, with a message that names the real problem.
        missing = [name for name, d in (('Project 1', dirs[0]), ('Project 2', dirs[1]))
                   if not [x for x in Directory.search_directories(d, exts) if x.strip()]]
        if missing:
            messages.error(
                request,
                'No %s files found for %s. Upload a folder containing %s files, '
                'or open the seeded demo-comparison project.'
                % (language, ' and '.join(missing), '/'.join(exts)))
            return render(request, "CodeClone/project_features.html", lang_ctx)

        nGram = request.POST.get('nGramRange', 2)
        try:
            res = model.run_test_Project(username=str(request.session['dir_dataset']),
                                         dirs=dirs, ngram=int(nGram), language=language)
        except Exception as e:
            print(e)
            messages.error(request, 'Comparison failed: %s' % e)
            return render(request, "CodeClone/project_features.html", lang_ctx)

        view_model = {'model': model}
        view_model.update(lang_ctx)
        return render(request, "CodeClone/project_features.html", view_model)

    return render(request, "CodeClone/project_features.html", lang_ctx)

def internal_projects(request):
    if request.method == 'GET':
        dirs = Directory.get_directory_of("projects/" + request.session['username'])
        projects = Directory.get_all_folders(dirs)
        return render(request, "CodeClone/internal_projects.html", {"projects": projects})
    return render(request, "CodeClone/internal_projects.html")

def internal_features(request, project_name=None):
    model = InternalProjectViewModel()
    if project_name is not None:
        username = request.session['username']
        dirs = Directory.get_directory_of("projects/"+username+"/"+project_name)
        request.session['dir_dataset'] = username+"/"+project_name
        request.session['dir_project'] = dirs

    if request.method == "POST":
        if 'dir_project' not in request.session or 'dir_dataset' not in request.session:
            messages.error(request, 'Open a project first, then run the scan.')
            return redirect('internal-projects')

        project_dir = str(request.session['dir_project'])
        language = HelperViewModel.get_project_language(project_dir)
        project_no = 2 if 'project2_features' in request.POST else 1
        source_dir = Directory.get_directory_of(project_dir + 'project' + str(project_no))

        # Internal clone compares files within one project, so it needs >= 2.
        exts = languages.get(language).extensions
        srcs = [x for x in Directory.search_directories(source_dir, exts) if x.strip()]
        if len(srcs) < 2:
            messages.error(
                request,
                'Internal clone needs at least 2 %s files in Project %d (found %d). '
                'Upload more files, or open the seeded internal-demo-%s project.'
                % (language, project_no, len(srcs), language))
            return render(request, "CodeClone/internal_features.html")

        try:
            model.run_test_Project(username=str(request.session['dir_dataset']),
                                   source_dir=source_dir, project_no=project_no, language=language)
        except Exception as e:
            print(e)
            messages.error(request, 'Scan failed: %s' % e)
            return render(request, "CodeClone/internal_features.html")

        return render(request, "CodeClone/internal_features.html", {'model': model})

    return render(request, "CodeClone/internal_features.html")

def delete_project(request, project_name):
    username = request.session['username']
    Directory.delete_dir('com/vsa/datasets/' + username+"/"+project_name)
    Directory.delete_dir("projects/"+username+"/"+project_name)
    return redirect('projects')

@login_required(login_url='/accounts/login/')
def languages_view(request):
    from .models import LanguageDefinition

    if request.method == 'POST':
        raw = request.POST.get('definition', '').strip()
        try:
            payload = json.loads(raw)
        except Exception as e:
            messages.error(request, 'Invalid JSON: %s' % e)
            return _render_languages(request, raw)

        errors = languages.validate_definition(payload)
        if errors:
            for err in errors:
                messages.error(request, err)
            return _render_languages(request, raw)

        name = str(payload['name']).strip().lower()
        LanguageDefinition.objects.update_or_create(
            name=name, defaults={'label': payload.get('label', ''), 'payload': payload})
        languages.register_definition(payload)
        messages.success(request, 'Added language "%s" (%s). Select it when creating a project.'
                         % (name, ', '.join(languages.get(name).extensions)))
        return redirect('languages')

    return _render_languages(request, None)


def _render_languages(request, definition_text):
    rows = []
    for name, label in languages.options():
        lang = languages.get(name)
        rows.append({'name': name, 'label': label,
                     'extensions': ', '.join(lang.extensions),
                     'tokens': len(lang.vocabulary),
                     'builtin': languages.is_builtin(name)})
    if definition_text is None:
        definition_text = json.dumps(languages.template(), indent=2)
    return render(request, 'CodeClone/languages.html',
                  {'language_rows': rows, 'definition_text': definition_text})


def reg(request):
    form = UserForm
    return render(request, "Accounts/registration_form.html", {'form': form})

def log(request):
    return render(request, "Accounts/login_form.html")


