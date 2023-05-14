from django.urls import path, include

from .views import ArticlesList, ArticlesDetail
from rest_framework import routers


# router = routers.SimpleRouter()
# router.register(r'articles', ArticlesViewSet)


urlpatterns = [
    path('', ArticlesList.as_view()),
    path('<int:pk>/', ArticlesDetail.as_view())
]