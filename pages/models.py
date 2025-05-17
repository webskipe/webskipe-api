from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

class Page(models.Model):
    """Farewell page model"""
    
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('private', 'Private'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    TONE_CHOICES = (
        ('celebratory', 'Celebratory'),
        ('grateful', 'Grateful'),
        ('reflective', 'Reflective'),
        ('humorous', 'Humorous'),
        ('emotional', 'Emotional'),
        ('professional', 'Professional'),
        ('dramatic', 'Dramatic'),
        ('poetic', 'Poetic'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    context = models.CharField(max_length=255, help_text="What are you saying goodbye to?")
    message = models.TextField()
    tone = models.CharField(max_length=50, choices=TONE_CHOICES)
    template = models.CharField(max_length=50)
    primary_color = models.CharField(max_length=20, default='#6D28D9')
    background_color = models.CharField(max_length=20, default='#ffffff')
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    expiry_date = models.DateField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a slug based on the title
            base_slug = slugify(self.title)
            
            # Check if the slug already exists
            if Page.objects.filter(slug=base_slug).exists():
                # If it exists, append a UUID
                self.slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
            else:
                self.slug = base_slug
                
        super().save(*args, **kwargs)

class PageMedia(models.Model):
    """Media files associated with a page"""
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='page_media/')
    file_type = models.CharField(max_length=20)  # image, video, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.page.title} - {self.file_type}"