from django.contrib import admin

from .models import Post, Comment

# Register your models here.
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'image', 'title', 'content', 'created')
    list_display = ('author', 'created', 'title')

