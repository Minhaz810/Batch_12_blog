from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampMixin):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class Post(TimeStampMixin):
    STATUS_CHOICES = [
        ('draft','DRAFT'),
        ('published','PUBLISHED'),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='draft')
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    def __str__(self):
        return f"{self.category}-{self.title}"


class Comment(TimeStampMixin):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
            to=User,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='comments'
        )
    body = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    def __str__(self):
        return f"{self.body}"
