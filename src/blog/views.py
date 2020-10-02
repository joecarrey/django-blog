from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
# from django.views.generic import (
# 	CreateView,
# 	DetailView,
# 	ListView,
# 	UpdateView,
# 	DeleteView
# )
from .models import Blog
from .forms import BlogModelForm

def BlogListView(request):
	blogs = Blog.objects.all().order_by('-id')
	content = {
		'blogs': blogs
	}
	return render(request, 'blogs/blog_list.html', content)

def BlogDetailView(request, id):
	content = {
		'blog': get_object_or_404(Blog, id=id)
	}
	return render(request, 'blogs/blog_detail.html', content)

def BlogMyListView(request):
	content = {
		'blogs': Blog.objects.filter(author_id=request.user.id)
	}
	return render(request, 'blogs/blog_mylist.html', content)

def BlogCreateView(request):
	my_form = BlogModelForm()
	if request.method == "POST": #   ?????????
		my_form = BlogModelForm(request.POST or None)
		if my_form.is_valid():
			obj = my_form.save(commit=False)
			obj.author = request.user
			obj.save()
		else:
			print(my_form.errors)
	context = {
		"form": my_form
	}
	return render(request, "blogs/blog_create.html", context)

def BlogUpdateView(request, id):
	blog = get_object_or_404(Blog, id=id)
	if request.user.id != blog.author_id:
		return render(request, 'home.html')
	my_form = BlogModelForm(request.POST or None, instance=blog)
	if my_form.is_valid():
		my_form.save()
		return HttpResponseRedirect(reverse("blogs:blog-detail", kwargs={"id": id}))
	return render(request, "blogs/blog_create.html", {'form': my_form})

def BlogDeleteView(request, id):
	blog = get_object_or_404(Blog, id=id)
	if request.user.id != blog.author_id:
		return render(request, 'home.html')
	if request.method == "POST":
		blog.delete()
		return HttpResponseRedirect(reverse("blogs:blog-list"))
	return render(request, 'blogs/blog_delete.html', {'blog': blog})

# class BlogListView(ListView):
# 	template_name = 'blogs/blog_list.html'
# 	queryset = Blog.objects.all()

# class BlogMyListView(ListView):
# 	template_name = 'blogs/blog_mylist.html'

# 	def get_queryset(self):
# 		return Blog.objects.filter(author_id=self.request.user.id)

# 	def form_valid(self, form):
# 		return super().form_valid(form)

# class BlogCreateView(CreateView):
# 	template_name = 'blogs/blog_create.html'
# 	form_class = BlogModelForm
# 	queryset = Blog.objects.all()
	
# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		return super().form_valid(form)

# class BlogDetailView(DetailView):
# 	template_name = 'blogs/blog_detail.html'
# 	model = Blog
	
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context["comments"] = Blog.comment_set
# 		return context

# class BlogUpdateView(UpdateView):
# 	template_name = 'blogs/blog_create.html'
# 	form_class = BlogModelForm
# 	queryset = Blog.objects.all()
	
# 	def post(self, request, *args, **kwargs):
# 		self.object = self.get_object()
# 		if self.request.user.id != self.object.author_id:
# 			return render(request, 'home.html')
# 		return super().post(request, *args, **kwargs)


# 	def form_valid(self, form):
# 		print(form.cleaned_data)
# 		return super().form_valid(form)

# class BlogDeleteView(DeleteView):
# 	template_name = 'blogs/blog_delete.html'
# 	queryset = Blog.objects.all()
	
# 	def delete(self, request, *args, **kwargs):
# 		self.object = self.get_object()
# 		if self.request.user.id != self.object.author_id:
# 			return render(request, 'home.html')
# 		return super().post(request, *args, **kwargs)

# 	# def get_object(self):
# 	# 	id_ = self.kwargs.get("id")
# 	# 	return get_object_or_404(Blog, id=id_)

# 	def get_success_url(self):
# 		return reverse('blogs:blog-list')
