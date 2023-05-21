from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe
from .serializers import UserSerializer, SubscribeSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.annotate(cnt=Count('articles')).order_by('-cnt')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class SubscribeView(generics.CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Отсутствует ключ PK'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user.id
        serializer = SubscribeSerializer(data=dict(user=user, author=pk))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Подписка оформлена'}, status=status.HTTP_201_CREATED)
