from __future__ import annotations

import re
from urllib.parse import urlparse

from django.core.files.storage import default_storage

from django_markdown_widget.settings import get_setting

# Matches markdown images ![alt](url) and links to uploaded files
_MEDIA_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def extract_media_urls(text: str) -> set[str]:
    """Extract all image URLs from markdown text."""
    if not text:
        return set()
    return set(_MEDIA_RE.findall(text))


def _url_to_storage_path(url: str) -> str | None:
    """Convert a media URL back to a storage path.

    Returns None if the URL doesn't look like an upload managed by this library.
    """
    upload_path_prefix = get_setting("UPLOAD_PATH").split("%")[0]
    parsed = urlparse(url)
    path = parsed.path

    idx = path.find(upload_path_prefix)
    if idx == -1:
        return None
    return path[idx:]


def delete_orphaned_media(old_text: str, new_text: str) -> list[str]:
    """Compare old and new markdown content, delete files that were removed.

    Returns list of deleted storage paths.
    """
    old_urls = extract_media_urls(old_text)
    new_urls = extract_media_urls(new_text)
    removed_urls = old_urls - new_urls

    deleted = []
    for url in removed_urls:
        storage_path = _url_to_storage_path(url)
        if storage_path and default_storage.exists(storage_path):
            default_storage.delete(storage_path)
            deleted.append(storage_path)
    return deleted
