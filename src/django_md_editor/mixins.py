from __future__ import annotations

from django.db.models import Model, TextField

from django_md_editor.cleanup import delete_orphaned_media
from django_md_editor.settings import get_setting


class MarkdownCleanupMixin(Model):
    """Model mixin that auto-deletes orphaned media when markdown fields change.

    Requires MD_EDITOR["CLEANUP_MEDIA"] = True in settings.

    Usage:
        class Post(MarkdownCleanupMixin, models.Model):
            content = models.TextField()

    To limit to specific fields:
        class Post(MarkdownCleanupMixin, models.Model):
            content = models.TextField()
            notes = models.TextField()
            markdown_cleanup_fields = ["content"]
    """

    markdown_cleanup_fields: list[str] | None = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._md_original_values = self._capture_markdown_fields()

    def _get_markdown_field_names(self) -> list[str]:
        if self.markdown_cleanup_fields is not None:
            return self.markdown_cleanup_fields
        return [f.name for f in self._meta.get_fields() if isinstance(f, TextField)]

    def _capture_markdown_fields(self) -> dict[str, str]:
        return {
            name: getattr(self, name, "") or ""
            for name in self._get_markdown_field_names()
        }

    def save(self, **kwargs):
        if get_setting("CLEANUP_MEDIA") and self.pk:
            new_values = self._capture_markdown_fields()
            for name, old_text in self._md_original_values.items():
                new_text = new_values.get(name, "")
                if old_text != new_text:
                    delete_orphaned_media(old_text, new_text)

        super().save(**kwargs)
        self._md_original_values = self._capture_markdown_fields()
