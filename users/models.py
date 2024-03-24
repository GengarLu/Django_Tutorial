from django.db import models
import uuid
# User是Django專案中auth應用程式所提供。
from django.contrib.auth.models import User

# Create your models here.

# null是針對資料庫而言，如果null=True，表示資料庫的該欄位可以為空。
# blank是針對表單的，如果blank=True，表示你的表單填寫該欄位的時候可以不填。
class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True, editable=False)
    # CASCADE代表違反參考完整性限制時，外來鍵所對應的資料將連帶刪除，update也是一樣
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True) # 住家地址
    short_intro = models.CharField(max_length=200, null=True, blank=True)# 簡短介紹
    bio = models.TextField(null=True, blank=True)# 個人簡介
    # upload_to='profiles/'上傳備份至static/images/profiles
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    # auto_now_add=True，表示新增一筆data時DateTime會自動添加當前時間
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username)
    
    class Meta:
        # 讓profiles依照優先級為:日期最舊-->日期最新
        ordering = ["date_posted"]
    
    @property # 可以將此函式做為屬性運行，而非一個function運行
    def imageURL(self):
        try: # 資料庫有profile_image的url時，抓取這個資料
            url = self.profile_image.url
        except: # 沒有時，給予空字串
            url = ""
        return url

class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True, editable=False)
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True) # 程式名稱
    description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
    
class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True, editable=False)
    # SET_NULL代表違反參考完整性限制時，外來鍵所對應的資料將設為NULL，update也是一樣
    # 但不使用CASCADE的原因是可能有用戶不小心刪除profile，這時回來註冊就需要有一些
    # 此用戶的message資訊
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True) # 寄件人
    # 因為sender也是關聯到Profile的FK，所以避免互相干擾，加上related_name="messages"
    recipient =  models.ForeignKey(Profile, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name="messages") # 收件人
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True) # 確認用戶是否讀取，預設為False
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    class Meta:
        # 讓messages依照優先級為:is_read(未讀~已讀) -> 創建messages最晚~最早(最新~最舊)來排序
        ordering = ["is_read", "-date_posted"]