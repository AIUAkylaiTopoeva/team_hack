from rest_framework import serializers
from .models import Post, Category, Rating, Favorites, Comment
# from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.contrib.auth import get_user_model
User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('title',)

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
        representation['favorite_count'] = instance.favorites.count()
        representation['likes_count'] = instance.likes.count()
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['comments'] = CommentCreateSerializers(Comment.objects.filter(post = instance.pk), many = True).data          #representation нужен для добавления comments в post
                                            
        return representation

class CommentCreateSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.name')
    class Meta:
        model = Comment
        fields = '__all__'
        # exclude = ('author',)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    # def validate_title(self, name):
    #     if self.Meta.model.objects.filter(name= name).exists():
    #         raise serializers.ValidationError('Песня с таким названием уже существует')
    #     # если ничего не ретернить, то оно не сохраниться в validated_data
    #     return name
    
    # def to_representation(self, instance):
    #     representation= super().to_representation(instance)
    #     representation['likes']= instance.likes.count()
    #     representation['rating']=instance.ratings.aggregate(Avg('rating'))['rating__avg']
    #     representation['favorite'] = instance.favorites.count()
    #     return representation
    
class RatingSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.name')
    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)
    
    def validate_rating(self, rating):
        if rating not in range(1,11):
            raise serializers.ValidationError('Рейтинг должен быть в промежутке от 1 до 10 включительно')
        return rating
    

