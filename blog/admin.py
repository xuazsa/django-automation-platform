from django.contrib import admin
from .models import Category, Tag, Post

@admin.action(description='发布选中的文章')
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'status', 'publish_time')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    actions = [make_published]  # 添加批量发布动作
