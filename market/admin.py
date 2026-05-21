from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    list_filter = ('available',)
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'price', 'quantity', 'subtotal')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'total_price', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    search_fields = ('customer_name', 'customer_email')
