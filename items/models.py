from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('ID card', 'ID card'),
        ('Bag', 'Bag'),
        ('Books', 'Books'),
        ('Others', 'Others'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items/')
    location = models.CharField(max_length=255)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_item = models.DateField() # When it was lost or found
    
    class Meta:
        abstract = True

class LostItem(Item):
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Lost: {self.name}"

class FoundItem(Item):
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Found: {self.name}"

class MatchResult(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='matches')
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name='matches')
    similarity_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-similarity_score']
