from django.urls import path
from .views import (
    comCreate,
    comDelete
)

app_name = 'comments'
urlpatterns = [
    path('create/<int:id>', comCreate, name='comment-create'),
    path('<int:id>/delete/', comDelete, name='comment-delete'),
]
