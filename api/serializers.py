"""
我們的SnippetSerializer類別正在複製模型中也包含的大量資訊Snippet(片段)。如果
我們的程式碼能夠更簡潔，那就太好了。就像Django同時提供Form類別和ModelForm類別
一樣，REST框架也包括Serializer(序列化器)類別和ModelSerializer類別。
"""
from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    # serializers.SerializerMethodField()是一種特殊的序列化器字段，
    # 它允許你添加一些自定義的字段到你的序列化器類。
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
    
    # serializers.SerializerMethodField()方法的名稱應該是get_<field_name>，
    # 其中<field_name>是上方定義的字段名(reviews)。
    def get_reviews(self, obj):
        # <model>_set是一種反向關聯，它允許你從一個模型對象訪問到與它相關的其他模型對象。
        # 它返回與obj相關的所有review對象。
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data