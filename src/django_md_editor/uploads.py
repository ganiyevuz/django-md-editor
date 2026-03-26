import time

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage

from django_md_editor.settings import get_setting


class BaseUploadHandler:
    def validate(self, file) -> None:
        pass

    def save(self, file) -> str:
        raise NotImplementedError


class DefaultUploadHandler(BaseUploadHandler):
    """Uses Django's default_storage backend."""

    def validate(self, file) -> None:
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

    def save(self, file) -> str:
        upload_path = get_setting("UPLOAD_PATH")
        timestamp = str(int(time.time()))
        path = time.strftime(upload_path) + timestamp + "_" + file.name
        saved_path = default_storage.save(path, file)
        return default_storage.url(saved_path)
