from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User =  get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(blank=True, primary_key=True, max_length=60)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs) :
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

# class Tag(models.Model):
#     title = models.CharField(max_length=60, unique=True)
#     slug = models.SlugField(blank=True, primary_key=True, max_length=60)   # B slug доступны только символы и underscore

#     def __str__(self) -> str:
#         return self.title
    
#     def save(self, *args, **kwargs) :
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save()

class Post(models.Model):
    name = models.CharField(max_length=30)

    description = models.TextField(blank=True)
    author =models.ForeignKey(User, on_delete=models.CASCADE ,max_length=40, related_name = 'posts', verbose_name='Автор') 
    artist = models.CharField(max_length=40)
    image = models.ImageField(upload_to='images/', blank = True)
    song = models.FileField(upload_to='musics/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Liked {self.post} by {self.author.name}'
    
class Favorites(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='favorites')
    is_saved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Liked {self.post} by {self.author.name}'
    
class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self) -> str:
        return f'You give {self.rating} stars to post {self.post}'
    
class Comment(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')   #related_name является(можем задавать через related_name) атрибутом класса
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Comment from {self.author.name} to {self.post.title}'
    