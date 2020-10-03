from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogMyListView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    likeBlog
)

app_name = 'blogs'
urlpatterns = [
	path('', BlogListView, name='blog-list'),
    path('mylist/', BlogMyListView, name='blog-mylist'),
    path('create/', BlogCreateView, name='blog-create'),
    path('<int:id>', BlogDetailView, name='blog-detail'),
    path('<int:id>/update/', BlogUpdateView, name='blog-update'),
    path('<int:id>/delete/', BlogDeleteView, name='blog-delete'),
    path('like/', likeBlog, name='blog-like'),
]
