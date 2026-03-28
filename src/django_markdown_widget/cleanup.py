from __future__ import annotations

import posixpath
import re
from urllib.parse import urlparse

from django.core.files.storage import default_storage

from django_markdown_widget.settings import get_setting

# Matches markdown images ![alt](url), links [text](url),
# and HTML src attributes (video, img, etc.)
_MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
_MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
_HTML_SRC_RE = re.compile(r'<(?:video|img|source|iframe)\s[^>]*src="([^"]+)"')


def extract_media_urls(text: str) -> set[str]:
    """Extract all media URLs from markdown text (images, videos, links)."""
    if not text:
        return set()
    urls = set()
    urls.update(_MD_IMAGE_RE.findall(text))
    urls.update(_MD_LINK_RE.findall(text))
    urls.update(_HTML_SRC_RE.findall(text))
    return urls


def _safe_resolve_path(url: str, prefix: str) -> str | None:
    """Extract and validate a storage path from a URL.

    Returns None if the URL doesn't match the prefix or contains
    path traversal components.
    """
    parsed = urlparse(url)
    path = parsed.path

    idx = path.find(prefix)
    if idx == -1:
        return None

    resolved = posixpath.normpath(path[idx:])

    # Reject path traversal
    if ".." in resolved.split("/"):
        return None

    # Must still start with the prefix after normalization
    if not resolved.startswith(prefix.rstrip("/")):
        return None

    return resolved


def _url_to_temp_path(url: str) -> str | None:
    """Convert a media URL to a temp storage path."""
    return _safe_resolve_path(url, get_setting("TEMP_UPLOAD_PATH"))


def _url_to_storage_path(url: str) -> str | None:
    """Convert a media URL back to a permanent storage path."""
    return _safe_resolve_path(url, get_setting("UPLOAD_PATH").split("%")[0])


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
