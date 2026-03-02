from django.contrib import admin
from .models import Profile, BlogPost

admin.site.register(Profile)

# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
admin.site.register(BlogPost, BlogPostAdmin)