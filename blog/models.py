from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User 
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    slug = models.SlugField(max_length = 50, unique = True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category_detail", kwargs={'slug': self.slug})
    

class Tag(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    slug = models.SlugField(max_length = 50, unique = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})
    

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'DRAFT'),
        ('published', 'PUBLISHED'),
    ]

    title = models.CharField(max_length = 200)
    slug = models.SlugField(max_length = 200, unique = True, blank = True)
    content = models.TextField()
    excerpt = models.TextField(max_length = 500, blank = True, help_text = "Brief description of the blog")

    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')
    status = models.CharField(max_length = 30, choices = STATUS_CHOICES, default = 'draft')

    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'posts')
    tags = models.ManyToManyField(Tag, blank = True, related_name = 'posts')
    
    featured_image = models.ImageField(upload_to = "blog/images/", blank = True, null = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    published_at = models.DateTimeField(null = True, blank = True)

    meta_description = models.CharField(max_length = 160, blank = True)
    meta_keywords = models.CharField(max_length = 255, blank =True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status == 'draft':
            self.published_at = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs = {'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_at is not None
    
    def get_reading_time(self):
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_comments')
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True, related_name = 'replies')

    content = models.TextField()
    is_approved = models.BooleanField(default = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta():
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    @property
    def is_reply(self):
        return self.parent is not None
    
    def get_replies(self):
        return self.replies.filter(is_approved = True)
    

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank = True)
    viewed_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = ['post', 'ip_address', 'viewed_at']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"View of {self.post.title} from {self.ip_address}"