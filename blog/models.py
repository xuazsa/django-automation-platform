from django.db import models
from django.utils import timezone

# 文章分类
class Category(models.Model):
    name = models.CharField('分类名称', max_length=50)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

# 文章标签
class Tag(models.Model):
    name = models.CharField('标签名称', max_length=50)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

# 文章模型
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL别名', max_length=200, unique=True)
    content = models.TextField('正文内容')
    summary = models.TextField('摘要', blank=True)
    
    # 外键关联
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    
    # 作者（关联 Django 内置用户）
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='作者')
    
    # 状态和发布时间
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='draft')
    publish_time = models.DateTimeField('发布时间', default=timezone.now)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-publish_time']
