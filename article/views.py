from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Article, ReadPost
from .serializers import ArticleSerializer, ReadPostSerializer
from .permissions import IsAdminOrAuthor


class ArticlesList(generics.ListCreateAPIView):
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminOrAuthor, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticlesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminOrAuthor, )


class ReadPostView(generics.CreateAPIView):
    queryset = ReadPost.objects.all()
    serializer_class = ReadPostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Отсутствует ключ PK'}, status=status.HTTP_400_BAD_REQUEST)
        article = Article.objects.get(pk=pk)
        user = self.request.user
        if len(ReadPost.objects.filter(user=user, article=article)) >= 1:
            return Response({'message': 'Статья уже прочитана'}, status=status.HTTP_409_CONFLICT)
        ReadPost.objects.create(article=article, user=user, read=True)
        return Response({'message': 'Прочитано'}, status=status.HTTP_201_CREATED)



