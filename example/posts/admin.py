from django.contrib import admin

from django_markdown_widget.admin import MarkdownEditorAdminMixin
from posts.models import Post


@admin.register(Post)
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    list_display = ["title", "created_at"]
    markdown_fields = ["content"]
