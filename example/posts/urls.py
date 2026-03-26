from django.urls import path

from posts.views import PostCreateView, PostDetailView, PostListView

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("create/", PostCreateView.as_view(), name="create"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
]
