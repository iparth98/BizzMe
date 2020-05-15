from django.urls import path
from .views import (
    add_to_cart,
    OrderSummaryView,
    CheckoutView,
    AddCouponView,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,

)

app_name = "ecommerce"
urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout_list"),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path("add-to-cart/<int:pk>/", add_to_cart, name='add-to-cart'),
    path("add-coupon/", AddCouponView.as_view(), name='add-coupon'),
    path("remove-from-cart/<int:pk>/", remove_from_cart, name='remove-from-cart'),
    path("remove-single-item-from-cart/<int:pk>/",
         remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path("payment/<payment_option>/", PaymentView.as_view(), name='payment'),
]
