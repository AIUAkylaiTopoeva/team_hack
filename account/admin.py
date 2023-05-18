from django.contrib import admin
from django.contrib.auth import get_user_model
# from .models import User
# Register your models here.
User= get_user_model()
# admin.site.register(User)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name','last_name','email')
    search_fields = ['name', 'last_name']
    ordering = ['name']
    list_display_links =['email']
    # list_filter=['is_active']
    # list_editable = ['is_staff']

admin.site.register(User, AccountAdmin)