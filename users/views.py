from django.shortcuts import render, redirect
# 用於authenticate()驗證一組憑證。它將憑證作為關鍵字參數，username對於 password
# 預設情況，根據每個身份驗證後端User檢查它們，如果憑證對於後端有效，則傳回一個物件。
# 若要從視圖登入用戶，請使用login()。login()使用 Django 的會話框架將使用者的 ID 保存在會話中。
from django.contrib.auth import authenticate, login, logout
# login_required用來保護特定template，也就是登入才能夠觀看或使用
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# UserCreationForm(新增使用者表單)及User，是Django專案中auth應用程式所提供。
# 繼承自UserCreationForm後，來進行客製化自己的註冊表單類別
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginationProfiles

# Create your views here.

def loginUser(request):
    page = 'login'

    # user.is_authenticated用戶登入且驗證通過
    if request.user.is_authenticated:
        return redirect('profiles') # 導回首頁

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        # try:
        #     user = User.objects.get(username=request.user)
        # except:
        #     messages.error(request, "Username does not exist")

        # 以下用來驗證database中的username及password是否等於上方的username及password
        user = authenticate(request, username=username, password=password)

        # 如果憑證對於任何後端都無效或後端引發PermissionDenied，則傳回None。
        if user is not None:
            login(request, user)
            """
            # request.GET['next']代表single_project.html的
            "?next={{request.path}}路徑"也就是當前要評論的project頁面
            # 如果'next'路徑存在GET method中就將導向至request.GET['next']
            else則導向至account.html頁面，這裡的else情況就是指點擊右上角login/register
            """
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "Username was logged out!")
    return redirect("login") # 導回登入畫面

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # commit=False -> save方法暫時不會將表單資料儲存到資料庫，而是給你返回一個當前物件。
            user = form.save(commit=False)
            # 當User表格的username = User表格的username的小寫
            user.username = user.username.lower()
            user.save() # 才儲存
            messages.success(request, "User account was created!") # 告知用戶註冊成功

            login(request, user) # 註冊完直接登入
            return redirect('profiles') # 再導回主頁，作者後來改成edit-account頁面，但我覺得沒必要
        else:
            messages.error(
                request, "An error has occurred during registration") # 告知用戶註冊失敗

    context = {'page' : page, 'form' : form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)
    page_array, profiles = paginationProfiles(request, profiles, 1)

    context = {'profiles' : profiles, 'search_query' : search_query, 
                'page_array' : page_array}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    # 從Skill資料表中排除所有description欄位為空字串的紀錄，並將結果
    # 存入topSkills。換句話說，topSkills將包含所有description
    # 欄位不為空字串的技能。
    topSkills = profile.skill_set.exclude(description__exact="")
    # 從Skill資料表中選出所有description欄位為空字串的紀錄，並將結果
    # 存入otherSkills。也就是說，otherSkills將包含所有description
    # 欄位為空字串的技能。
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile' : profile, 'topSkills' : topSkills, 
                'otherSkills' : otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    # 等於上方的profile = Profile.objects.get(id=pk)，
    # 只是變向去抓網站session中的資料
    profile = request.user.profile
    
    # Account頁面因為只有個人看的到，所以不太注重描述有無為空
    # topSkills = profile.skill_set.exclude(description__exact="")
    # otherSkills = profile.skill_set.filter(description="")
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile' : profile, 'skills' : skills, 'projects' : projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    # 等於上方的profile = Profile.objects.get(id=pk)，
    # 只是變向去抓網站session中的資料
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        # 有圖片，所以要FILES
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account') # 更新完導回account頁面

    context = {'form' : form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    # 等於上方的profile = Profile.objects.get(id=pk)，
    # 只是變向去抓網站session中的資料
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            # commit=False -> save方法暫時不會將表單資料儲存到資料庫，而是給你返回一個當前物件。
            skill = form.save(commit=False)
            # 當Skill表格的owner = 當前登入user
            skill.owner = profile
            skill.save() # 才儲存
            messages.success(request, "Skill was added successfully!")
            return redirect("account") # 導向至account.html

    context = {'form' : form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    # 等於上方的profile = Profile.objects.get(id=pk)，
    # 只是變向去抓網站session中的資料
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk) # 只query Skill中user所對應的skill
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect("account") # 導向至account.html

    context = {'form' : form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url="login")
def deleteSkill(request, pk):
    # 等於上方的profile = Profile.objects.get(id=pk)，
    # 只是變向去抓網站session中的資料
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk) # 只query Skill中user所對應的skill
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect("account") # 導向至account.html
    context = {'object' : skill}
    return render(request, "delete_template.html", context)

@login_required(login_url="login")
# inbox訊息收件夾
def inbox(request):
    # 等於上方的profile = Profile.objects.get(id=pk)，
    # 只是變向去抓網站session中的資料
    profile = request.user.profile
    # 補充一點:為何不是messages_set，因為models.py的Message表格有兩個FK，
    # 在抓取資料時會衝突所以其中recipient設為related_name="messages"，
    # 讓profile.messages.all()去抓有關聯的recipient
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count() # 未讀訊息數
    context = {'messageRequests' : messageRequests, 'unreadCount' : unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url="login")
def viewMessage(request, pk):
    # 等於上方的profile = Profile.objects.get(id=pk)，
    # 只是變向去抓網站session中的資料
    profile = request.user.profile
    message = profile.messages.get(id=pk) # Message表格id=pk的資料
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message' : message}
    return render(request, 'users/message.html', context)

def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk) # 當前要發送message的developer
    form = MessageForm()

    try:
        sender = request.user.profile # 當前用戶
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # commit=False -> save方法暫時不會將表單資料儲存到資料庫，而是給你返回一個當前物件。
            message = form.save(commit=False)
            # 當Message表格的sender = 當前登入user
            message.sender = sender
            # 當Message表格的recipient = 當前要發送message的developer
            message.recipient = recipient

            # 因為登入狀態的message form沒有name和email，所以在這主動發送
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save() # 才儲存
            messages.success(request, "Your messages were successfully sent!")
            # 導向至pk=recipient.id(要發送message的developer)的user-profile.html
            return redirect("user-profile", pk=recipient.id)

    context = {'recipient' : recipient, 'form' : form}
    return render(request, 'users/message_form.html', context)