from .models import Profile, Skill
# Q 物件將 SQL 表達式封裝在 Python 物件中，該物件可用於與資料庫相關的操作。
# 使用 Q 物件，我們可以使用更少和更簡單的程式碼進行複雜查詢。
from django.db.models import Q
# Paginator：幫助管理分頁數據，即透過「上一頁/下一頁」連結分割到多個頁面的數據。
# PageNotAnInteger：當傳遞給page()的頁碼不是整數時，會引發此異常。
# EmptyPage：當傳遞給page()的頁碼不在有效範圍內(例如，頁碼過大或過小，或者數據為空時)，會引發此異常。
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginationProfiles(request, profiles, curr_results):

    current_page = request.GET.get('page') # 要顯示的頁數
    results = curr_results # 一頁顯示的資料數
    paginator = Paginator(profiles, results) # results放進來

    # 如果current_page不是整數，則返回第一頁(PageNotAnInteger)；如果current_page超出範圍，
    # 則返回最後一頁(EmptyPage)。這樣可以確保用戶始終看到有效的頁面，而不會看到錯誤。
    try:
        profiles = paginator.page(current_page)
    except PageNotAnInteger:
        current_page = 1
        profiles = paginator.page(current_page)
    except EmptyPage:
        current_page = paginator.num_pages
        profiles = paginator.page(current_page)

    # pagination有很多頁數時的呈現方式
    page_array = []
    if paginator.num_pages > 4:
        # 假設現在總頁數15頁，當前在第4頁結果:12345…15。
        if(int(current_page) < 5):
            for count in range(1, 6):
                page_array.append(count)
            
            page_array.append('...')
            page_array.append(paginator.num_pages)

        else: # 假設現在總頁數15頁，當前在第11頁結果:1…11 12 13 14 15。
            end_limit = paginator.num_pages - 5
            if int(current_page) > end_limit:
                page_array.append(1)
                page_array.append('...')
                for count in range(end_limit + 1, paginator.num_pages + 1):
                    page_array.append(count)
            else: # 假設現在總頁數15頁，當前在第10頁結果:1…9 10 11…15。
                page_array.append(1)
                page_array.append('...')
                for count in range(int(current_page) - 1, int(current_page) + 2):
                    page_array.append(count)
                page_array.append('...')
                page_array.append(paginator.num_pages)
    else: # 假設現在總頁數小於4頁(全部顯示)結果:1 2 3。
        for count in range(1, paginator.num_pages + 1):
            page_array.append(count)

    return page_array, profiles

def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    # 查詢Skill表格中的name
    skills = Skill.objects.filter(name__icontains=search_query)

    # attribute__icontains是有包含value且不區分大小寫的data
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains = search_query) | 
        Q(short_intro__icontains = search_query) | 
        Q(skill__in = skills) # 並塞到skill__in變數
    )

    return profiles, search_query