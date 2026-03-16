from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_available']  # edit directly from list
    ordering = ['-created_at']


# CartItem inline - show cart items inside cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # no extra empty rows


# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    inlines = [CartItemInline]  # show cart items inside cart


# OrderItem inline - show order items inside order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # no extra empty rows


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_price', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'full_name', 'email']
    list_editable = ['status']  # update status directly from list
    ordering = ['-created_at']
    inlines = [OrderItemInline]  # show order items inside order