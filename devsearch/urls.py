"""
URL configuration for devsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # 為了串接settings.py中的MEDIA_ROOT和MEDIA_URL
from django.conf.urls.static import static # 幫助我們為靜態文件創建URL
# 幫助我們做下方的email password reset功能
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
    path('api/', include('api.urls')),

    # 1 - 使用者提交電子郵件以進行重置   //PasswordResetView.as_view()           //name="reset_password"
    # 2 - 電子郵件發送訊息              //PasswordResetDoneView.as_view()       //name="passsword_reset_done"
    # 3 - 包含連結和重置說明的電子郵件   //PasswordResetConfirmView.as_view()  //name="password_reset_confirm"
    # 4 - 密碼成功重置訊息              //PasswordResetCompleteView.as_view()   //name="password_reset_complete"
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), 
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), 
         name="password_reset_done"),
    # <uidb64>/<token>/以base64加密方式對用戶的ID進行編碼
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
         name="password_reset_complete"),
]

# 串接settings.py中的MEDIA_ROOT和MEDIA_URL
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# 串接settings.py中的STATIC_ROOT和STATIC_URL
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)