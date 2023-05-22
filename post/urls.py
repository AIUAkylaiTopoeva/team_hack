from django.urls import path, include
from .views import CategoryListView, PostViewSet, CommentView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentView)
router.register('category', CategoryListView)
# router.register('favorites', FavoriteViewSet)

urlpatterns = [
    # path('categories/', CategoryListView.as_view()),
    path('', include(router.urls)),
    path('music/', views.index , name='index'),
]