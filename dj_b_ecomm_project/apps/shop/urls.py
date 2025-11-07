# shop/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    # Products urls
    path('stock-product-list', views.stock_products_list_view, name="stock_products_list"),
    path('create-stock-product/', views.create_stock_product_view, name='create_stock_product'),
    path('products/update-stock-update/<int:pk>/', views.update_stock_product_view, name='update_stock_product'),
    path('delete-stock-product/<int:pk>/', views.delete_stock_product_view, name='delete_stock_product'),
    path('stock-product-detail/<int:pk>/', views.stock_product_detail_view, name='stock_product_detail'),
    
    # comments /review
    path('review/like/<int:pk>/', views.like_review, name='like_review'),
    path('review/dislike/<int:pk>/', views.dislike_review, name='dislike_review'),
    
]