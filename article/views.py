from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Article, ReadPost
from .serializers import ArticleSerializer
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


# class ReadPostView(generics.CreateAPIView):
#     queryset = ReadPost.objects.all()
#     serializer_class = ReadPostSerializer
#     permission_classes = (IsAuthenticated,)



