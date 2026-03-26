from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from posts.forms import PostForm
from posts.models import Post


class PostListView(ListView):
    model = Post
    template_name = "posts/list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create.html"
    success_url = reverse_lazy("posts:list")


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/detail.html"
    context_object_name = "post"
