from django.urls import path
from api_v2.views import get_csrf_token, ArticleView, CommentView

app_name = 'api_v2'

urlpatterns = [
    path('get-token/', get_csrf_token, name='get_token'),
    path('articles/', ArticleView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleView.as_view(), name='article'),
    path('articles/<int:article_pk>/comments/', CommentView.as_view(), name='comments'),
    path('articles/<int:article_pk>/comments/<int:pk>/', CommentView.as_view(), name='comment'),
]
