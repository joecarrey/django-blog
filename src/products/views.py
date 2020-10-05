from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import (
	ListView,
	CreateView,
	DetailView,
	UpdateView,
	DeleteView,
	View
)
from .models import *
from .forms import ProductModelForm, ReviewModelForm

class ProductListView(ListView):
	template_name = 'products/product_list.html'
	queryset = Product.objects.filter(active=True)
	context_object_name = 'products'

class ProductMyListView(ListView):
	model = Product
	template_name = 'products/product_mylist.html'
	context_object_name = 'products'

	def get_queryset(self):
		return Product.objects.filter(owner_id=self.request.user.id)

class ProductCreateView(CreateView):
	template_name = 'products/product_create.html'
	form_class = ProductModelForm
	queryset = Product.objects.all()
	
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

class ProductDetailView(DetailView):
	model = Product
	template_name = 'products/product_detail.html'
	context_object_name = 'product'

	def get_context_data(self, **kwargs):
		is_liked = False
		if self.object.likes.filter(id=self.request.user.id).exists():
			is_liked = True
		context = super().get_context_data(**kwargs)
		context["is_liked"] = is_liked
		context["total_likes"] = self.object.total_likes()
		return context

class ProductUpdateView(UpdateView):
	template_name = 'products/product_create.html'
	form_class = ProductModelForm
	queryset = Product.objects.all()

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.request.user.id != self.object.owner_id:
			return render(request, 'home.html')
		return super().post(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
	template_name = 'products/product_delete.html'
	queryset = Product.objects.all()
	
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.request.user.id != self.object.owner_id:
			return render(request, 'home.html')
		return super().delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse("products:product-mylist")

def likeProduct(request):
	product = get_object_or_404(Product, id=request.POST.get('like'))
	is_liked = False
	if product.likes.filter(id=request.user.id).exists():
		product.likes.remove(request.user)
		is_liked = False
	else:
		product.likes.add(request.user)
		is_liked = True
	return HttpResponseRedirect(reverse("products:product-detail", kwargs={"pk": request.POST.get('like')}))

###############################################    REVIEW   ###############################################

class ReviewCreateView(CreateView):
	template_name = 'products/review_create.html'
	form_class = ReviewModelForm
	queryset = Review.objects.all()
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.product_id = self.kwargs['pk']
		return super().form_valid(form)


class ReviewDeleteView(DeleteView):
	template_name = 'products/review_delete.html'
	queryset = Review.objects.all()
	
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.request.user.id != self.object.author_id:
			return render(request, 'home.html')
		return super().delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse("products:product-detail", kwargs={"pk": self.object.product.pk})