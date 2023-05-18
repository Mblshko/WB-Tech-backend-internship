from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.annotate(cnt=Count('articles')).order_by('-cnt')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
