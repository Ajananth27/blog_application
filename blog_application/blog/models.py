from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

class Blog(Base):
    title = models.CharField(max_length=250, blank=True, null=True)
    content = models.TextField()
    author = models.CharField(max_length=32, blank=True, null=True)
    publication_date = models.DateTimeField(default=timezone.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "blog"

class Comment(Base):
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE, related_name="blog_comment")
    commenter_name = models.CharField(max_length=32, blank=True)
    email = models.EmailField(null=True, blank=True)
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = "comment"
