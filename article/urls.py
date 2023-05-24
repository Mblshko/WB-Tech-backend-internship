from django.urls import path, include
from rest_framework import routers
from .views import ArticlesViewSet, ReadArticleView


router = routers.DefaultRouter()
router.register(r'', ArticlesViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/read/', ReadArticleView.as_view(), name='article_read')
]