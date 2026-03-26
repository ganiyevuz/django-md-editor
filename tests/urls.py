from django.urls import include, path

urlpatterns = [
    path("md-editor/", include("django_md_editor.urls")),
]
