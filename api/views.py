# @api_view 是一個裝飾器，用於將基於函數的視圖轉換為 API view。這個裝飾器
# 接受一個 HTTP 方法的列表作為參數，例如 @api_view(["GET", "POST", "DELETE"])
# ，這表示該視圖只能處理 GET 和 POST 和 DELETE請求
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

@api_view(['GET']) # 用於處理基於函數的views的decorator裝飾器。
def getRoutes(request):
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'}, # 當有人點擊id=當前id的projects並進行投票時採用POST請求
        
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'}, # 當用戶的token過期時，要確保仍可以保持登入狀態，所以需要refresh token
    ]
    # JsonResponse 用於將Python字典或其他可JSON序列化的數據轉換為JSON格式，並將其作為HTTP響應返回給客戶端。
    # safe=False的作用是允許JsonResponse返回非字典對象，如果嘗試在safe=True的情況下返回非字典對象，Django
    # 會拋出一個TypeError。如果您需要返回一個列表或其他非字典對象，您應該將safe參數設置為False。這樣，
    # Django就不會對返回數據進行安全性檢查。
    # return JsonResponse(routes, safe=False)
    return Response(routes)

@api_view(['GET']) # 用於處理基於函數的views的decorator裝飾器。
# 是一個decorator，它用於設置視圖(view)或視圖集(viewset)的權限類。
# IsAuthenticated是一個內置的權限類，它要求用戶必須已經認證(也就是登錄)
# 才能訪問該視圖或視圖集。
# @permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    # many=True是用於指定序列化器(Serializer)應該序列化一個查詢集(QuerySet)或多個對象，
    # 而不僅僅是一個單一對象。查詢集(QuerySet)或多個對象代表資料表的"指定多個"欄位資料
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET']) # 用於處理基於函數的views的decorator裝飾器。
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # many=False是用於指定序列化器(Serializer)應該序列化一個單一對象，
    # 單一對象代表資料表的"指定單一"欄位資料
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data # POST的相關資料
    serializer = ProjectSerializer(project, many=False)
    
    # get_or_create()它嘗試根據給定的查詢參數獲取一個對象。如果找到了符合查詢
    # 參數的對象，它就會返回這個對象；如果沒有找到，它就會創建一個新的對象。
    # created是一個布林值，如果創建了新的對象，則為True，否則為False。
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project, # 右邊的project是models.py中Review的project欄位
    )

    review.value = data['value'] # value就是up(贊成)或down(反對)
    review.save()
    # models.py中Project的getVoteCount()欄位(屬性)，也就是總票數和贊成率
    project.getVoteCount

    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagID = request.data['tag']
    projectID = request.data['project']

    project = Project.objects.get(id=projectID)
    tag = Tag.objects.get(id=tagID)

    project.tags.remove(tag)

    return Response("Tag was deleted!")