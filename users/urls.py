from django.urls import path

from .views import UserViewSet, SubscribeViewSet


urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('<int:pk>/sub/', SubscribeViewSet.as_view({'post': 'create'})),
    path('<int:pk>/unsub/', SubscribeViewSet.as_view({'delete': 'destroy'})),
]