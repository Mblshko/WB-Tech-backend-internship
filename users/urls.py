from django.urls import path

from .views import UserViewSet, SubscribeViewSet, ShowSubArticlesViewSet


urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('<int:pk>/sub/', SubscribeViewSet.as_view({'post': 'create'})),
    path('<int:pk>/unsub/', SubscribeViewSet.as_view({'delete': 'destroy'})),
    path('sublist/', ShowSubArticlesViewSet.as_view({'get': 'show_sub_article'}))
]