import json

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializators import ArticleSerializer, CommentSerializer
from webapp.models import Article, Comment


# Create your views here.

@ensure_csrf_cookie
def get_csrf_token(request):
    if request.method == 'GET':
        return HttpResponse()
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


class ArticleView(APIView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            article = get_object_or_404(Article, pk=kwargs['pk'])
            serializer = ArticleSerializer(article, many=False)
            return Response(serializer.data)
        else:
            articles = Article.objects.order_by('-created_at')
            serializer = ArticleSerializer(articles, many=True)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        serializer = ArticleSerializer(data=body)
        if serializer.is_valid():
            article = serializer.save()
            return JsonResponse(
                {'pk': article.pk, 'title': article.title, 'content': article.content, 'status': article.status},
                status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        body = json.loads(request.body)
        serializer = ArticleSerializer(data=body, instance=article)
        if serializer.is_valid():
            article = serializer.save()
            article_data = ArticleSerializer(article).data
            return JsonResponse(article_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'errors': serializer.errors}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return JsonResponse({'message': 'Статья была успешно удалена'}, status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    def get(self, request, article_pk=None, pk=None, *args, **kwargs):
        if pk:
            comment = get_object_or_404(Comment, pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif article_pk:
            article = get_object_or_404(Article, pk=article_pk)
            comments = article.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'Id статьи обязателен'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, article_pk=None, *args, **kwargs):
        if article_pk:
            article = get_object_or_404(Article, pk=article_pk)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(article=article)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Id статьи обязателен чтобы оставить комментарий'},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({'message': 'Комментарий был успешно удален'}, status=status.HTTP_204_NO_CONTENT)
