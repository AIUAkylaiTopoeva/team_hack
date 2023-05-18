from django.contrib import admin
from .models import Category, Post,Like, Favorites, Comment, Rating
# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Favorites)
admin.site.register(Comment)
admin.site.register(Rating)