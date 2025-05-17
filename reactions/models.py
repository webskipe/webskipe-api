from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from pages.models import Page

class Reaction(models.Model):
    """Model for reactions (likes, hearts, etc.)"""
    
    REACTION_CHOICES = (
        ('like', 'Like'),
        ('heart', 'Heart'),
        ('clap', 'Clap'),
        ('laugh', 'Laugh'),
        ('sad', 'Sad'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        # Ensure a user can only leave one type of reaction per page
        unique_together = ('user', 'page', 'reaction_type')
    
    def __str__(self):
        return f"{self.user.username} - {self.reaction_type} - {self.page.title}"

class Comment(models.Model):
    """Model for comments on pages"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.page.title}"