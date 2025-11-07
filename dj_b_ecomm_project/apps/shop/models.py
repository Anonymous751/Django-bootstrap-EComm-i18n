

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [('electronics', _("Electronics")),
    ('tech', _("Tech")),
    ('sports', _("Sports")),
    ('fashion', _("Fashion")),
    ('home', _("Home & Kitchen")),
                        ]
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to="products/")
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default='electronics')
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_reviews')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='disliked_reviews')

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()


    
