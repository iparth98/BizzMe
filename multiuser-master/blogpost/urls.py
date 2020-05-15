from django.urls import path

from .views import (
    post_list,
    post_create,
    post_update,
    post_delete,
    PostDetailView,
    UserPostListView
)
app_name = "blogpost"
urlpatterns = [
    path('', post_list, name='post-list'),
    path('create/', post_create, name='post-create'),
    path('<slug>/', PostDetailView.as_view(), name='detail'),
    path('<slug>/edit/', post_update, name='post-update'),
    path('<slug>/delete/', post_delete, name='post-delete'),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),

]