from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    # null是針對資料庫而言，如果null=True，表示資料庫的該欄位可以為空。
    # blank是針對表單的，如果blank=True，表示你的表單填寫該欄位的時候可以不填。
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    # 個人照，放一個預設照片(default.jpg)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # 在這創建一個與下方的Tag table多對多關係，'Tag'代表接到下方的class Tag
    tags = models.ManyToManyField('Tag', blank=True)
    # 把Tag的value放至Project table，並顯示其vote_total和vote_ratio
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # auto_now_add=True，表示新增一筆data時DateTime會自動添加當前時間
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        # 讓projects依照優先級為:降序的vote_ratio -> 降序的vote_total -> title來排序
        ordering = ["-vote_ratio", "-vote_total", "title"]

    @property # 可以將此函式做為屬性運行，而非一個function運行
    def imageURL(self):
        try: # 資料庫有featured_image的url時，抓取這個資料
            url = self.featured_image.url
        except: # 沒有時，給予空字串
            url = ""
        return url

    @property # 可以將此函式做為屬性運行，而非一個function運行
    def reviewers(self):
        """
        # review_set.all()會返回與當前實例(self)相關的所有評論。
        # values_list('owner__id', flat=True)這是一個查詢集方法，
        它會返回一個包含所有評論者 ID 的列表。"owner__id" 是查詢的
        欄位，"flat=True" 表示返回一個單一維度的列表。
        """
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property # 可以將此函式做為屬性運行，而非一個function運行
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count() # 贊成票
        totalVotes = reviews.count() # 總票數
        ratio = (upVotes / totalVotes) * 100 # 贊成率

        # 將上方即時計算的totalVotes和ratio更新至Project表格的vote_total和vote_ratio
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True, editable=False)
    # CASCADE代表違反參考完整性限制時，外來鍵所對應的資料將連帶刪除，update也是一樣
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=1000, null=True, blank=True) # 內容主體
    # 給user兩個選項，讓user決定是否支持這個review
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # 是否支持兩選項存至value
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        # unique_together功能是將多個值綁在一起，所以利用這個功能後
        # 就不能具有相同的owner和相同的project資料，目的是避免有心人士
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                        primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
