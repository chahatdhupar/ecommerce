from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import ProductForm, CheckoutForm


# Home page - show all products
def home(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })


# Product detail page
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {
        'product': product
    })


# Search products
def search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    if category_id:
        products = products.filter(category__id=category_id)

    return render(request, 'store/search.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
    })


# Add product to cart
@login_required(login_url='login')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('cart')


# View cart
@login_required(login_url='login')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    return render(request, 'store/cart.html', {
        'cart': cart,
        'items': items
    })


# Remove item from cart
@login_required(login_url='login')
def remove_from_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id)

    if cart_item.cart.user == request.user:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    else:
        messages.error(request, 'You are not allowed to do this!')

    return redirect('cart')


# Update cart item quantity
@login_required(login_url='login')
def update_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id)

    if cart_item.cart.user == request.user:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        messages.success(request, 'Cart updated!')
    else:
        messages.error(request, 'You are not allowed to do this!')

    return redirect('cart')


# Checkout page
@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.cartitem_set.all()

    if not items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

    form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total()
            order.save()

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            items.delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'items': items,
        'form': form
    })


# Order success page
@login_required(login_url='login')
def order_success(request):
    return render(request, 'store/order_success.html')


# Order history page
@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {
        'orders': orders
    })


# Order detail page
@login_required(login_url='login')
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    items = order.orderitem_set.all()
    return render(request, 'store/order_detail.html', {
        'order': order,
        'items': items
    })
