from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Blog(models.Model):
	title	= models.CharField(max_length=120)
	content = models.TextField()
	active	= models.BooleanField(default=True)
	author 	= models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	likes 	= models.ManyToManyField(User, related_name='likes', blank=True)

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse("blogs:blog-detail", kwargs={"id": self.id})