from django.urls import path
from . import views # 導入views的各項def，至於用.是因為urls和views在同一層

urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>', views.project, name="project"),
    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<str:pk>', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>', views.deleteProject, name="delete-project"),
]