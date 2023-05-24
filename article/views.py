from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Article, ReadArticle
from .serializers import ArticleSerializer, ReadArticleSerializer
from .permissions import IsAdminOrAuthor


class ArticlesViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrAuthor]

    def get_queryset(self):
        queryset = Article.objects.filter(is_published=True)
        read_filter = self.request.query_params.get('read', None)
        if read_filter == 'True':
            queryset = queryset.filter(read__read=1)
        elif read_filter == 'False':
            queryset = queryset.exclude(read__read=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReadArticleView(generics.CreateAPIView):
    queryset = ReadArticle.objects.all()
    serializer_class = ReadArticleSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Отсутствует ключ PK'}, status=status.HTTP_400_BAD_REQUEST)
        article = Article.objects.get(pk=pk)
        user = self.request.user
        if len(ReadArticle.objects.filter(user=user, article=article)) >= 1:
            return Response({'message': 'Статья уже прочитана'}, status=status.HTTP_409_CONFLICT)
        ReadArticle.objects.create(article=article, user=user)
        return Response({'message': 'Прочитано'}, status=status.HTTP_201_CREATED)
