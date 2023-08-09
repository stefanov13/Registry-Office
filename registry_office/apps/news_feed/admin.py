from django.contrib import admin
from .models import NewsFeedModel

# Register your models here.

@admin.register(NewsFeedModel)
class NewFeedAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    list_display = ('title', 'description', 'author', 'date',)
    list_filter = ('title', 'description', 'author', 'date',)
    search_fields = ('title', 'description', 'author', 'date',)
