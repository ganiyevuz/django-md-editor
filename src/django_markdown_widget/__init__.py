__version__ = "2.0.0"

from django_markdown_widget.admin import MarkdownEditorAdminMixin  # noqa: E402
from django_markdown_widget.cleanup import (  # noqa: E402
    delete_orphaned_media,
    extract_media_urls,
)
from django_markdown_widget.renderers import BaseRenderer, DefaultRenderer  # noqa: E402
from django_markdown_widget.uploads import (  # noqa: E402
    BaseUploadHandler,
    DefaultUploadHandler,
)
from django_markdown_widget.widgets import MarkdownEditorWidget  # noqa: E402


def __getattr__(name):
    if name == "MarkdownCleanupMixin":
        from django_markdown_widget.mixins import MarkdownCleanupMixin

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
