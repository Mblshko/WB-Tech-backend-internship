from django.urls import path

from .views import UserList, UserDetail, SubscribeView


urlpatterns = [
    path('', UserList.as_view()),
    path('<int:pk>/', UserDetail.as_view()),
    path('<int:pk>/sub/', SubscribeView.as_view())
]