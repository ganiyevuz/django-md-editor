from django.urls import path

from django_markdown_widget.views import FinalizeView, UploadView

app_name = "django_markdown_widget"

urlpatterns = [
    path("upload", UploadView.as_view(), name="upload"),
    path("finalize", FinalizeView.as_view(), name="finalize"),
]
