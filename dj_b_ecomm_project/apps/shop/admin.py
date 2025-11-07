from django.contrib import admin
from .models import Product, Review
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'images', 'is_featured', 'is_trending', 'created_at']
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'likes_count', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['user__username', 'product__name', 'comment']