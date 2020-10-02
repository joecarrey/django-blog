from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Comment
from blog.models import Blog
from .forms import CommentModelForm

def comCreate(request, id):
	blog = get_object_or_404(Blog, id=id)
	my_form = CommentModelForm()
	if request.method == "POST":
		my_form = CommentModelForm(request.POST or None)
		if my_form.is_valid():
			obj = my_form.save(commit=False)
			obj.author = request.user
			obj.blog = blog
			obj.save()
			return HttpResponseRedirect(reverse("blogs:blog-detail", kwargs={"id": id}))
		else:
			print(my_form.errors)
	context = {
		"form": my_form
	}
	return render(request, "comments/comment_create.html", context)

def comDelete(request, id):
	comment = get_object_or_404(Comment, id=id)
	if request.user.id != comment.author_id:
		return render(request, 'home.html')
	if request.method == "POST":
		comment.delete()
		return HttpResponseRedirect(reverse("blogs:blog-detail", kwargs={"id": comment.blog.id}))
	return render(request, 'comments/comment_delete.html', {'comment': comment})