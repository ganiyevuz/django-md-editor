__version__ = "1.0.0"

from django_md_editor.admin import MarkdownEditorAdminMixin  # noqa: E402
from django_md_editor.cleanup import (  # noqa: E402
    delete_orphaned_media,
    extract_media_urls,
)
from django_md_editor.renderers import BaseRenderer, DefaultRenderer  # noqa: E402
from django_md_editor.uploads import (  # noqa: E402
    BaseUploadHandler,
    DefaultUploadHandler,
)
from django_md_editor.widgets import MarkdownEditorWidget  # noqa: E402


def __getattr__(name):
    if name == "MarkdownCleanupMixin":
        from django_md_editor.mixins import MarkdownCleanupMixin

        return MarkdownCleanupMixin
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "MarkdownEditorWidget",
    "MarkdownEditorAdminMixin",
    "MarkdownCleanupMixin",
    "BaseRenderer",
    "DefaultRenderer",
    "BaseUploadHandler",
    "DefaultUploadHandler",
    "delete_orphaned_media",
    "extract_media_urls",
]
