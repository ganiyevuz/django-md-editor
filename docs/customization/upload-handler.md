# Custom Upload Handler

The upload handler validates and stores files uploaded through the editor.

## Default Handler

`DefaultUploadHandler` validates MIME types and file size, then stores files using Django's `default_storage` backend with timestamped filenames.

## Creating a Custom Handler

Subclass `BaseUploadHandler` and implement `save`. Optionally override `validate`:

```python
import uuid
from django_md_editor import BaseUploadHandler

class S3UploadHandler(BaseUploadHandler):
    def validate(self, file):
        if file.size > 5 * 1024 * 1024:
            from django.core.exceptions import ValidationError
            raise ValidationError("Files must be under 5 MB.")

    def save(self, file) -> str:
        import boto3
        s3 = boto3.client("s3")
        key = f"uploads/{uuid.uuid4()}/{file.name}"
        s3.upload_fileobj(file, "my-bucket", key)
        return f"https://my-bucket.s3.amazonaws.com/{key}"
```

### Requirements

- `validate(file)` -- raise `django.core.exceptions.ValidationError` to reject the file. Called before `save`.
- `save(file)` -- store the file and return a URL string. This URL is inserted into the markdown content as `![filename](url)`.

## Register Your Handler

```python
MD_EDITOR = {
    "UPLOAD_HANDLER_CLASS": "myapp.uploads.S3UploadHandler",
}
```
