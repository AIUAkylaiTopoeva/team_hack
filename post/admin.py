from django.contrib import admin
from .models import Category, Post, Rating, Like, Comment


admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Comment)

class RatingInline(admin.TabularInline):
    model = Rating


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'category', 'get_rating', 'get_likes', 'song', 'get_favorites')
    inlines = [RatingInline]
    search_fields = ['title', 'body']
    ordering = ['created_at']
    list_filter = ['category__title']

    def get_rating(self, obj):
        from django.db.models import Avg
        result = obj.ratings.aggregate(Avg('rating'))
        return result['rating__avg']

    def get_likes(self, obj):
        result = obj.likes.count()
        return result

    def get_favorites(self, obj):
        result = obj.favorites.count()
        return result

admin.site.register(Post, PostAdmin)