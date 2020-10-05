from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Product(models.Model):
	title		= models.CharField(max_length=120)
	description = models.TextField()
	active		= models.BooleanField(default=True)
	owner 		= models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	likes 		= models.ManyToManyField(User, related_name='p_likes', blank=True)

	def __str__(self):
		return self.title

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs={"pk": self.pk})

	def total_likes(self):
		return self.likes.count()

class Review(models.Model):
	body 	= models.TextField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
	author 	= models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	def __str__(self):
		return self.product.title + ' review'

	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs={"pk": self.product.pk})