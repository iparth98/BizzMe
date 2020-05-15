from django.urls import include, path

from .views import users, customers, business
from ecommerce.views import ItemDetailView, ItemCreateView, BusinessItemListView

urlpatterns = [
    path('validate/', users.accountvalidation, name='validate'),
    path('', users.HomeView.as_view(), name='home'),
    path("product/<int:pk>/", ItemDetailView.as_view(), name="product_list"),
    path('products/<str:username>',
         BusinessItemListView.as_view(), name='business-product-list'),
    path('customers/', include(([
        path('', customers.customer_home, name='customer-dashboard'),

    ], 'users'), namespace='customers')),
    # ....................................................................................
    path('business/', include(([
        path('', business.business_home, name='business-dashboard'),
        path('business_create/', business.BusinessCreateView.as_view(),
             name='business-form'),
        path("info/<int:pk>/", business.BusinessDetailView.as_view(),
             name='business-info'),
        path('create-item/', ItemCreateView.as_view(), name='create-item'),

    ], 'userpanel'), namespace='businesses')),
]
