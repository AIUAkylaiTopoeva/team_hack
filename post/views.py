from django.shortcuts import render
from rest_framework import generics, filters, viewsets
from .models import Rating, Post, Category, Favorites, Like, Comment
from .serializers import PostSerializer, RatingSerializers, CategorySerializer, FavoritesSerializer, CommentCreateSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsOwnerPermission, IsAdminOrActivePermission
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status_code=201, headers=headers)

class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.all()      
    serializer_class = PostSerializer
    filter_backends=[DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'artist']
    search_fields = ['name', 'artist']
    ordering_fields = ['created_at', 'name']

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action =='create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.parser_classes= [AllowAny]
        return super().get_permissions()
    
    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['post']=pk
        # print(data)
        rating = Rating.objects.filter(author = request.user,post=pk).first()
        # print(rating)
        serializer = RatingSerializers(data=data, context= {'request': request})
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('You do rating. Patch thid')
            # if request.method =='POST':
            #     serializer.create(serializer.validated_data)
            #     return Response(serializer.data)
            elif rating and request.method =='PATCH':
                serializer.update(rating, serializer.validated_data)
                return Response(serializer.data, status=204)
            elif request.method =='POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data, status=201)
            

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author = user)
            like.delete()
            message = 'dislike'
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, author = user, is_liked = True)
            like.save()
            message = 'liked'
        return Response(message, status=201)
    
    # is_favorite= True
class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['post__name', 'post__artist']

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializers

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action =='create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.parser_classes= [AllowAny]
        return super().get_permissions()