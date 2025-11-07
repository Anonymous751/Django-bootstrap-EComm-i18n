from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from apps.cart.models import CartItem
from .models import Product, Review
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=403)

    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
    user=request.user,
    product=product,
    defaults={'quantity': 1}  # new items always start with 1
)

    cart_items = CartItem.objects.filter(user=request.user)
    cart_data = [
        {
            'id': item.id,
            'name': item.product.name,
            'quantity': item.quantity,
            'total_price': float(item.product.price) * item.quantity,
            'image': item.product.images.url if item.product.images else '',
        }
        for item in cart_items
    ]

    cart_total = sum(float(i.product.price) * i.quantity for i in cart_items)
    cart_count = cart_items.count()

    # NEW: create new_item for frontend
    new_item = {
        'id': cart_item.id,
        'name': cart_item.product.name,
        'quantity': cart_item.quantity,
        'total_price': float(cart_item.product.price) * cart_item.quantity,
        'image': cart_item.product.images.url if cart_item.product.images else '',
    }

    return JsonResponse({
        'success': True,
        'message': f'{product.name} added to cart!',
        'cart_items': cart_data,
        'cart_total': cart_total,
        'cart_count': cart_count,
        'new_item': new_item,  # ✅ added
    })


def update_cart_item(request):
    if request.method == "POST" and request.user.is_authenticated:
        item_id = request.POST.get("item_id")
        action = request.POST.get("action")

        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
            message = "Quantity increased!"
        elif action == "decrease":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                message = "Item removed from cart!"
            else:
                cart_item.save()
                message = "Quantity decreased!"
        else:
            message = ""

        # Prepare response
        cart_items = CartItem.objects.filter(user=request.user)
        cart_list = [{
            "id": item.id,
            "name": item.product.name,
            "quantity": item.quantity,
            "total_price": float(item.total_price),
            "image": item.product.images.url
        } for item in cart_items]

        cart_total = sum(item.total_price for item in cart_items)
        cart_count = cart_items.count()  # total unique items

        return JsonResponse({
            "success": True,
            "cart_items": cart_list,
            "cart_total": float(cart_total),
            "cart_count": cart_count,
            "message": message
        })
    return JsonResponse({"success": False}, status=400)


def get_cart_data(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_list = [{
        'id': item.id,
        'name': item.product.name,
        'quantity': item.quantity,
        'total_price': item.total_price,
        'image': item.product.images.url
    } for item in cart_items]

    cart_total = sum(item.total_price for item in cart_items)
    cart_count = sum(item.quantity for item in cart_items)

    return JsonResponse({
        'success': True,
        'cart_items': cart_list,
        'cart_total': cart_total,
        'cart_count': cart_count
    })


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    cart_items = CartItem.objects.filter(user=request.user)
    items_with_total = []
    cart_total = 0

    for item in cart_items:
        total_price = item.product.price * item.quantity
        cart_total += total_price
        items_with_total.append({
            'id': item.id,
            'product': item.product,
            'quantity': item.quantity,
            'total_price': total_price
        })

    return render(request, 'components/checkout.html', {
        'cart_items': items_with_total,
        'cart_total': cart_total
    })
    
def stock_products_list_view(request):
    # Group products by category
    categories = {}
    all_products = Product.objects.all().order_by('category', '-created_at')
    
    for product in all_products:
        categories.setdefault(product.get_category_display(), []).append(product)  # type: ignore

    # Add the ModelForm for the modal
    form = ProductForm()

    # Handle form submission
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('stock_products_list')  # Refresh page to show new product

    context = {
        'categories': categories,
        'form': form,  # send form to template
    }
    return render(request, 'shop/stock_products_list.html', context)


def create_stock_product_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('stock_products_list')  # redirect to product list page
        else:
            messages.error(request, 'Failed to create product. Please check the form.')
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'shop/create_product.html', context)


def update_stock_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('stock_products_list')  # Redirect to product list after saving
    else:
        form = ProductForm(instance=product)
    
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'shop/update_stock_product.html', context)


def delete_stock_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product "{product.name}" has been deleted successfully!')
        return redirect('stock_products_list')  # Change this to your product list page URL name

    return redirect('stock_products_list')  # fallback if method is not POST


def stock_product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Handle review form submission
    if request.method == "POST":
        if request.user.is_authenticated:
            rating = request.POST.get("rating", 5)
            comment = request.POST.get("comment", "")
            if comment.strip():  # optional: only save if comment is not empty
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
            return redirect('stock_product_detail', pk=product.pk)
        else:
            return redirect('accounts:login')  # or your login URL

    context = {
        'product': product
    }
    return render(request, 'shop/stock_product_detail.html', context)



@login_required
def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    user = request.user

    if user in review.likes.all():
        review.likes.remove(user)  # remove like (toggle)
    else:
        review.likes.add(user)
        review.dislikes.remove(user)  # remove dislike if any

    return redirect('stock_product_detail', pk=review.product.pk)


@login_required
def dislike_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    user = request.user

    if user in review.dislikes.all():
        review.dislikes.remove(user)
    else:
        review.dislikes.add(user)
        review.likes.remove(user)  # remove like if any

    return redirect('stock_product_detail', pk=review.product.pk)