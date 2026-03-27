from django.urls import path

from django_markdown_widget.views import PreviewView, UploadView

app_name = "django_markdown_widget"

urlpatterns = [
    path("preview", PreviewView.as_view(), name="preview"),
    path("upload", UploadView.as_view(), name="upload"),
]
