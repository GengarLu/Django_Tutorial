from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects), # 資料表的"指定多個"欄位資料
    path('projects/<str:pk>', views.getProject), # 資料表的"指定單個"欄位資料
    path('projects/<str:pk>/vote/', views.projectVote), # 資料表的"指定單個"vote資料

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('remove-tag/', views.removeTag),
]