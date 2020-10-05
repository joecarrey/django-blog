from django.urls import path
from .views import *

app_name = 'products'
urlpatterns = [
	path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('mylist/', ProductMyListView.as_view(), name='product-mylist'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('like/', likeProduct, name='product-like'),

    path('<int:pk>/review/create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/review/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
