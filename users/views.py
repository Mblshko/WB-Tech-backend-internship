from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from article.models import Article
from .models import Subscribe
from .serializers import UserSerializer, SubscribeSerializer
from article.serializers import ArticleSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        '''
        Отображение пользователей с возможностью сортировки по кол-ву статей
        '''
        queryset = self.get_queryset()
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            if ordering == 'up':
                queryset = queryset.annotate(total=Count('articles')).order_by('-total')
            elif ordering == 'down':
                queryset = queryset.annotate(total=Count('articles')).order_by('total')
        serializer = UserSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(pk=kwargs.get('pk'))
        if queryset:
            serializer = UserSerializer(instance=queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Subscribe.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            user = self.request.user.id
            serializer = SubscribeSerializer(data=dict(user=user, author=pk))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Подписка оформлена'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Отсутствует ключ PK'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        author = User.objects.get(pk=pk)
        if pk:
            instance = Subscribe.objects.filter(user=self.request.user, author=pk)
            if instance:
                instance.delete()
                return Response({'message': f'Вы успешно отписались от {author.username}'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': f'Вы не были подписаны на {author.username}'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Такого пользователя не существует'}, status=status.HTTP_400_BAD_REQUEST)


class ShowSubArticlesViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Subscribe.objects.filter(user=self.request.user)
        queryset_article = Article.objects.none()
        for item in queryset:
            article = Article.objects.filter(author=item.author, created_at__gt=item.date_sub)
            if article:
                queryset_article |= article
        return queryset_article

    def show_sub_article(self, request):
        queryset_article = self.get_queryset()
        response = super(ShowSubArticlesViewSet, self).list(queryset_article, request)
        if queryset_article:
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(response.data, status=status.HTTP_204_NO_CONTENT)
