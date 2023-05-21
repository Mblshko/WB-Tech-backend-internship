from django.urls import path

from .views import ArticlesList, ArticlesDetail, ReadArticleView


urlpatterns = [
    path('', ArticlesList.as_view(), name='articles_list'),
    path('<int:pk>/', ArticlesDetail.as_view(), name='article_detail'),
    path('<int:pk>/read/', ReadArticleView.as_view(), name='article_read')
]