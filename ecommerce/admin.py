from django.contrib import admin
from .models import Item, Order, OrderItem, Payment, Coupon
from django.contrib.auth.models import User


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Coupon)
