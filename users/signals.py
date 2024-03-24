# User是Django專案中auth應用程式所提供。
from django.contrib.auth.models import User
# post_save將會在資料儲存時發送signals，post_delete則是刪除時發送
from django.db.models.signals import post_save, post_delete
# receiver裝飾器用於將一個函數註冊為信號接收器。換句話說，
# 信號允許某些發送者通知一組接收器，某些操作已經發生。
from django.dispatch import receiver
from .models import Profile
# Django在SMTP lib上提供了一些輕量級包裝器。提供這些包裝器是為了使發送電子郵件
# 變得更加快速，幫助在開發過程中測試電子郵件發送，並為無法使用 SMTP 的平台提供支援。
from django.core.mail import send_mail
# settings的其中一項功能可以幫助開發者節省手動輸入寄件人的email
from django.conf import settings

# @receiver(post_save, sender=Profile)
# created用來判斷database中是否添加了新紀錄，所以輸出是boolean
# **kwargs 是用來接收任意數量的關鍵字參數
def createProfile(sender, instance, created, **kwargs):
    print("Profile signal triggered") # 訊號已觸發
    if created:
        user = instance # 這裡的instance是database中的User
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

        # Send Email
        subject = "Welcome to DevSearch"
        message = "We are glad you are here!"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, # 寄件人email
            [profile.email], # 收件人email
            # 布林值。當作email的例外處理，如果有error會引發smtplib.SMTPException
            fail_silently=False,
        )

# 在edit-account頁面更新的資料是Profile的，那麼就需要連帶把User的資料也更新
def updateUser(sender, instance, created, **kwargs):
    profile = instance # 這裡的instance是database中的Profile
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    # try except為了處理從Users表單刪除user資料會出現"user query doesn't exist"
    try:
        user = instance.user # 這裡的instance是database中的Profile
        user.delete()
    except:
        pass

# 在sender=User時觸發post_save.connect
post_save.connect(createProfile, sender=User)
# 在sender=Profile時觸發post_save.connect
post_save.connect(updateUser, sender=Profile)
# 在sender=Profile時觸發post_delete.connect
post_delete.connect(deleteUser, sender=Profile)