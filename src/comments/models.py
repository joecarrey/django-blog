from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog
from django.urls import reverse

class Comment(models.Model):
	body 	= models.TextField()
	blog 	= models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)
	author 	= models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	def get_absolute_url(self):
		return reverse("blogs:blog-detail", kwargs={"id": self.id})