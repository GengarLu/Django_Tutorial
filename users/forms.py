from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {'first_name' : 'Name'} # 將first_name的label改成Name

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
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        """
        這部份是為了將project_form.html的{{field}}都加上class="input"，
        才能使css的樣式添加上去。而self.fields是字典，所以name, field
        代表key, value
        """
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        # fields = ['name', 'email', 'username', 
        # 'location', 'bio', 'short_intro', 'profile_image', 
        # 'social_github', 'social_twitter', 'social_linkedin', 
        # 'social_youtube', 'social_website']
        fields = '__all__'
        exclude = ['user'] # 欄位排除user不顯示

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):

    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner'] # 欄位排除owner不顯示

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})