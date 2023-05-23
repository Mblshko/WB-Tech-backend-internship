from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Subscribe
from .serializers import UserSerializer, SubscribeSerializer


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    @action(detail=False, permission_classes=[IsAuthenticated])
    def list(self, request, *args, **kwargs):
        '''
        Отображение всех пользователей с будущей возможностью сортировки
        '''
        queryset = self.get_queryset().order_by('?')
        serializer = UserSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(pk=kwargs.get('pk'))
        if queryset:
            serializer = UserSerializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        queryset = Subscribe.objects.all()
        return queryset

    @action(detail=True, permission_classes=[IsAuthenticated])
    def create(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            user = self.request.user.id
            serializer = SubscribeSerializer(data=dict(user=user, author=pk))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Подписка оформлена'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Отсутствует ключ PK'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            instance = Subscribe.objects.filter(user=self.request.user, author=pk)
            if instance:
                instance.delete()
                return Response({'message': f'Вы успешно отписались'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': f'Вы не были подписаны'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Такого пользователя не существует'}, status=status.HTTP_400_BAD_REQUEST)
