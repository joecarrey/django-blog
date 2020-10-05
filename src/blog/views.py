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
	blog = get_object_or_404(Blog, id=id)
	is_liked = False
	if blog.likes.filter(id=request.user.id).exists():
		is_liked = True
	content = {
		'blog': blog,
		'is_liked': is_liked,
		'total_likes': blog.total_likes()
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

def likeBlog(request):
	blog = get_object_or_404(Blog, id=request.POST.get('like'))
	is_liked = False
	if blog.likes.filter(id=request.user.id).exists():
		blog.likes.remove(request.user)
		is_liked = False
	else:
		blog.likes.add(request.user)
		is_liked = True
	return HttpResponseRedirect(reverse("blogs:blog-detail", kwargs={"id": request.POST.get('like')}))
