from rest_framework import serializers
from .models import Category, Post, Rating, Comment,Favorite
from django.contrib.auth import get_user_model
from django.db.models import Avg

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', )

 
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('author',)

    def validate_title(self, title):
        # if self.Meta.model.objects.filter(title=title).exists():
        if Post.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'Пост с таким заголовком уже существует'
            )
        return title
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = Post.objects.create(author=user, **validated_data)
        return post
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentCreateSerializer(Comment.objects.filter(post=instance.pk), many=True).data
        representation['favorite_count'] = instance.favorites.count()
        representation['likes_count'] = instance.likes.count()
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
                                            
        return representation


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def validte_rating(self, rating):
        if rating not in range(1, 11):
            raise serializers.ValidationError(
                'Рейтинг должен быть от 1 до 10'
            )
        return rating

    def create(self, validated_data):
        user = self.context.get('request').user
        rating = Rating.objects.create(author = user, **validated_data)
        return rating


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'




class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('author',)

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author = user, **validated_data)
        return comment
