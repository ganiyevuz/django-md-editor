from django.urls import path

from django_md_editor.views import PreviewView, UploadView

app_name = "django_md_editor"

urlpatterns = [
    path("preview/", PreviewView.as_view(), name="preview"),
    path("upload/", UploadView.as_view(), name="upload"),
]
