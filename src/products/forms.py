from django import forms

from .models import *

class ProductModelForm(forms.ModelForm):

	class Meta:
		model = Product
		fields =[
			'title',
			'description'
		]

class ReviewModelForm(forms.ModelForm):

	class Meta:
		model = Review
		fields =[
			'body',
		]