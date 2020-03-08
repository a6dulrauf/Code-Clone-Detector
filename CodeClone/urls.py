
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('projects/', views.projects, name='projects'),
    path('project-features/', views.project_features, name='project-features'),
    path('project-features/<project_name>', views.project_features, name='project-features'),

    path('internal-projects/', views.internal_projects, name='internal-projects'),
    path('internal-features/', views.internal_features, name='internal-features'),
    path('internal-features/<project_name>', views.internal_features, name='internal-features'),

    path('delete-project/', views.delete_project, name='delete-project'),
    path('delete-project/<project_name>', views.delete_project, name='delete-project'),

    path('contact-us/', views.contact_us, name='contact-us'),
    path('reg/', views.reg, name='reg'),
    path('log/', views.log, name='log'),
]