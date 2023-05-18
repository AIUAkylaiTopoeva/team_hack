from django.urls import path, include
from .views import PostViewset, CategoryListView , CommentViewset

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('posts',PostViewset)
router.register('comments', CommentViewset)

urlpatterns = [
    path('categories/',CategoryListView.as_view()),
    # path('tags/',TagListView.as_view() ),
    # path('comments/', CommentViewset.as_view()),
    # path('posts/', PostViewset.as_view({'get' : 'list'})),
    path('',include(router.urls))
]