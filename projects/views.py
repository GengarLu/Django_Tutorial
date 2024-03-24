from django.shortcuts import render, redirect
from django.http import HttpResponse #可幫助我們將view的內容返回HttpResponse
# login_required用來保護特定template，也就是登入才能夠觀看或使用
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginationProjects

# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    page_array, projects = paginationProjects(request, projects, 3)

    context = {'projects' : projects, 'search_query' : search_query, 'page_array' : page_array}
    return render(request, 'projects/projects.html', context)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm() # 代表上方import的ReviewForm

    if request.method == 'POST': # 如果single-project.html的<form method='POST'>符合
        # ReviewForm的fields丢到form,且資料有效的話儲存
        form = ReviewForm(request.POST)
        if form.is_valid():
            # commit=False -> save方法暫時不會將表單資料儲存到資料庫，而是給你返回一個當前物件。
            review = form.save(commit=False)
            # 當前端review的project = Project表格的資料
            review.project = projectObj
            # 當前端review的owner = 當前登入user
            review.owner = request.user.profile
            review.save() # 才儲存
            
            # 將models.py中的def getVoteCount(self)置入，計算總票數和贊成率
            projectObj.getVoteCount

            # 更新project投票數成功提示
            messages.success(request, "Your review was successfully submitted!")

            return redirect("project", pk=projectObj.id) # 將當前所評論的project_id重新導向一次

    context = {'project' : projectObj, 'form' : form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm() # 代表上方import的ProjectForm

    if request.method == 'POST': # 如果project_form.html的<form method='POST'>符合
        # project_form.html中的name="newtags"的textbox，用戶新增tags的間隔方法都不同，
        # 例如:"html, css, js"、"html css js"，那我們就統一將間隔方法replace(',', ' ')
        newtags = request.POST.get("newtags").replace(',', ' ').split()

        # ProjectForm的fields丢到form,且資料有效的話儲存
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False -> save方法暫時不會將表單資料儲存到資料庫，而是給你返回一個當前物件。
            project = form.save(commit=False)
            # 當前端project的owner = 當前登入user
            project.owner = profile
            project.save() # 才儲存

            for tag in newtags:
                # 抓取新增的tag內容，用created(boolean)判斷新增的內容是否重複
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag) # 對Project表單的tags欄位添加新的tag

            return redirect("account") # 導向至account.html

    context = {'form' : form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    # project = Project.objects.get(id=pk) # 改成下面
    project = profile.project_set.get(id=pk) # 只query Profile中user所對應的project
    form = ProjectForm(instance=project) # 代表上方import的ProjectForm

    if request.method == 'POST': # 如果project_form.html的<form method='POST'>符合
        # project_form.html中的name="newtags"的textbox，用戶新增tags的間隔方法都不同，
        # 例如:"html, css, js"、"html css js"，那我們就統一將間隔方法replace(',', ' ')
        newtags = request.POST.get("newtags").replace(',', ' ').split()

        # ProjectForm的fields丢到form,且資料有效的話儲存
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                # 抓取新增的tag內容，用created(boolean)判斷新增的內容是否重複
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag) # 對Project表單的tags欄位添加新的tag

            return redirect("account") # 導向至account.html

    context = {'form' : form, 'project':project}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    # project = Project.objects.get(id=pk) # 改成下面
    project = profile.project_set.get(id=pk) # 只query Profile中user所對應的project
    if request.method == 'POST':
        project.delete()
        return redirect("projects") # 導向至projects.html
    context = {'object':project}
    return render(request, "delete_template.html", context)