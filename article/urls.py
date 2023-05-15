from django.urls import path

from .views import ArticlesList, ArticlesDetail, ReadPostView


urlpatterns = [
    path('', ArticlesList.as_view()),
    path('<int:pk>/', ArticlesDetail.as_view()),
    path('<int:pk>/read/', ReadPostView.as_view())
]