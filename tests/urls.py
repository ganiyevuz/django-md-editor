from django.urls import include, path

urlpatterns = [
    path("md-editor/", include("django_markdown_widget.urls")),
]
