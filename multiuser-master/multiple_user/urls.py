"""multiple_user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from userpanel.views import customers, users, business
from userpanel.views import users as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userpanel.urls')),
    path('', include('ecommerce.urls', namespace='ecommerce')),
    path('posts/', include("blogpost.urls", namespace='posts')),
    path('about/', users.about, name='about'),
    path('contact/', users.contact, name='contact'),
    path('profile/', user_views.profile, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', users.loginfunc, name='signin'),
    path('accounts/signups/', users.SignUpView.as_view(), name='signup'),
    path('accounts/signup/customer/',
         customers.CustomerSignUpView.as_view(), name='customers_signup'),
    path('accounts/signup/business/',
         business.BusinessSignUpView.as_view(), name='business_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
# error aigi..