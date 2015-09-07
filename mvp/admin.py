from django.contrib import admin
from .models import Photo, Comment

# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url', 'user', 'description')
    search_fields = ('user',)

admin.site.register(Photo, PhotoAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'content')

admin.site.register(Comment, CommentAdmin)