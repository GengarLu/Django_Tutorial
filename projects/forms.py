from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    """
    模型的元數據，指的是“除了欄位外的所有內容”，例如排序方式、資料庫表名、人類可讀的單數或
    複數名等等。所有的這些都是非必須的，甚至元資料本身對模型也是非必須的。但是，我要說但是
    ，有些元資料選項能給予你極大的幫助，在實際使用上具有重要的作用，是實際應用的'必須'。
    想在模型中增加元數據，方法很簡單，在模型類中加入一個子類，名字是固定的Meta，然後在這個
    Meta類下面增加各種元數據選項或者說設定項。參考下面的例子：
    https://www.liujiangblog.com/course/django/99
    """
    class Meta:
        model = Project # 代表上方import的Project
        # 代表models.py的Project中所有欄位
        fields = ["title", "featured_image", "description",
                 "demo_link", "source_link"]

        # 為了將tags的樣式改為checkbox
        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        }

    """
    __init__ 是一個特殊的方法，稱為類的初始化方法。當你創建一個新的 ProjectForm 實例時
    ，Python 會自動調用這個方法。
    在 __init__ 方法中，*args 和 **kwargs 是用來接收任意數量的位置參數和關鍵字參數。
    這樣做的目的是為了能夠將這些參數傳遞給父類的 __init__ 方法。
    super(ProjectForm, self).__init__(*args, **kwargs) 這行程式碼的作用是調用父類
    (也就是 ModelForm)的 __init__ 方法，並將所有的參數傳遞給它。這樣可以確保父類的初
    始化工作被正確地完成。
    """
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        """
        這部份是為了將project_form.html的{{field}}都加上class="input"，
        才能使css的樣式添加上去。而self.fields是字典，所以name, field
        代表key, value
        """
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

        # self.fields['title'].widget.attrs.update({'class':'input'})
        # self.fields['description'].widget.attrs.update({'class':'input'})
        # ......等同上方的for迴圈
            
class ReviewForm(ModelForm):
    class Meta:
        model = Review # 代表上方import的Review
        # 代表models.py的Review中value與body欄位
        fields = ["value", "body"]
        labels = {
            'value' : "Place your vote",
            'body' : "Add a comment with your vote",
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        """
        這部份是為了將single-project.html的{{field}}都加上class="input"，
        才能使css的樣式添加上去。而self.fields是字典，所以name, field
        代表key, value
        """
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})