from django.shortcuts import render, get_object_or_404
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'myapp/home.html', {'posts': posts})

def about(request):
    return render(request, 'myapp/about.html')

def post_detail(request, pk):  # Change post_id to pk
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'myapp/post_detail.html', {'post': post})
