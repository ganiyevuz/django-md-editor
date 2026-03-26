from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("md-editor/", include("django_md_editor.urls")),
    path("", include("posts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
