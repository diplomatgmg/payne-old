from django.contrib import admin

from .models import CartItem, PromoCode, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 2


@admin.register(PromoCode)
class CouponCodeAdmin(admin.ModelAdmin):
    fields = ('promo_code', 'discount',)
    list_display = ('promo_code', 'discount')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'street', 'house', 'building', 'apartment',
                    'phone', 'email', 'description', 'created', 'updated')
    fields = (('first_name', 'last_name', 'email', 'phone'), ('city', 'street', 'house', 'building', 'apartment'),
              'description', ('total_price', 'real_price', 'discount'), ('created', 'updated'))

    readonly_fields = ('created', 'updated')
    inlines = (OrderItemInline,)
