from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=120, primary_key=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=40)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts') 
    song = models.FileField(blank=True,null=True, upload_to='songs')
    audio_link = models.CharField(max_length=200,blank=True,null=True)



class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self) -> str:
        return f'Liked {self.post} by  {self.author.name}'
    

class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    is_favorite = models.BooleanField(default=False) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self) -> str:
        return f'favotite {self.post} by {self.author.name}'
    

class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self) -> str:
        return f'this {self.post} rated by {self.author} for {self.rating}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.author.name}  to  {self.post.title}'

