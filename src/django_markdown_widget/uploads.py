from __future__ import annotations

import os
import re
import time
from abc import ABC, abstractmethod

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile

from django_markdown_widget.settings import get_setting

_SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]")
_MAX_FILENAME_LEN = 200


def sanitize_filename(name: str) -> str:
    """Strip path components and unsafe characters from a filename."""
    name = os.path.basename(name)
    name = _SAFE_FILENAME_RE.sub("_", name)
    if len(name) > _MAX_FILENAME_LEN:
        stem, ext = os.path.splitext(name)
        name = stem[: _MAX_FILENAME_LEN - len(ext)] + ext
    return name or "upload"


class BaseUploadHandler(ABC):
    def validate(self, file: UploadedFile) -> None:  # noqa: B027
        pass

    @abstractmethod
    def save(self, file: UploadedFile) -> str: ...


class DefaultUploadHandler(BaseUploadHandler):
    """Uses Django's default_storage backend."""

    def validate(self, file: UploadedFile) -> None:
        allowed_types = get_setting("ALLOWED_UPLOAD_TYPES")
        if file.content_type not in allowed_types:
            raise ValidationError(
                f"File type '{file.content_type}' is not allowed. "
                f"Allowed types: {', '.join(allowed_types)}"
            )
        max_size = get_setting("MAX_UPLOAD_SIZE")
        if file.size > max_size:
            raise ValidationError(
                f"File size {file.size} bytes exceeds maximum of {max_size} bytes."
            )

    def save(self, file: UploadedFile) -> str:
        temp_path = get_setting("TEMP_UPLOAD_PATH")
        timestamp = str(int(time.time()))
        safe_name = sanitize_filename(file.name)
        path = temp_path + timestamp + "_" + safe_name
        saved_path = default_storage.save(path, file)
        return default_storage.url(saved_path)

    @staticmethod
    def finalize(temp_url: str) -> str:
        """Move a file from temp to permanent storage. Returns new URL."""
        from django_markdown_widget.cleanup import _url_to_temp_path

        temp_path = _url_to_temp_path(temp_url)
        if not temp_path or not default_storage.exists(temp_path):
            return temp_url

        filename = temp_path.rsplit("/", 1)[-1]
        filename = sanitize_filename(filename)
        upload_path = get_setting("UPLOAD_PATH")
        permanent_path = time.strftime(upload_path) + filename
        permanent_path = default_storage.save(
            permanent_path, default_storage.open(temp_path)
        )
        default_storage.delete(temp_path)
        return default_storage.url(permanent_path)
