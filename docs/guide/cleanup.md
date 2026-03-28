# Media Cleanup

When users upload files to the editor and later remove them from the content, the files remain in storage. The cleanup system handles this at multiple levels.

## Temp Upload System

Uploads go to temporary storage first (`md-editor/tmp/`). When the form is submitted, the editor calls the `/finalize` endpoint which:

1. Scans the markdown content for referenced temp URLs
2. Moves referenced files to permanent storage (`md-editor/uploads/YYYY/MM/`)
3. Replaces temp URLs with permanent URLs in the content

Files that were uploaded but removed before saving stay in `tmp/` and are cleaned up by the management command.

## Model Mixin (Automatic)

`MarkdownCleanupMixin` hooks into `save()` to compare old and new content and delete files that were removed.

```python
from django.db import models
from django_markdown_widget import MarkdownCleanupMixin

class Post(MarkdownCleanupMixin, models.Model):
    content = models.TextField()
```

Enable in settings:

```python
MD_EDITOR = {
    "CLEANUP_MEDIA": True,
}
```

### Limiting to Specific Fields

By default, the mixin tracks all `TextField` instances on the model. To limit cleanup to specific fields:

```python
class Post(MarkdownCleanupMixin, models.Model):
    content = models.TextField()       # tracked
    internal_notes = models.TextField() # not tracked

    markdown_cleanup_fields = ["content"]
```

### How It Works

1. On model instantiation, the mixin captures the current values of tracked fields
2. On `save()`, it compares old values to new values
3. For each changed field, it extracts image/video/document URLs from both versions
4. URLs present in the old text but absent in the new text are identified as orphans
5. Orphaned files are deleted from Django's `default_storage`

!!! note
    Cleanup only runs on updates (when `pk` is set). New objects skip the check since there's no previous content to compare against.

## Management Command (Bulk)

For existing data or periodic maintenance, use the management command:

```bash
# Preview what would be deleted
python manage.py cleanup_markdown_media --dry-run

# Delete orphaned files
python manage.py cleanup_markdown_media
```

The command handles two phases:

**1. Expired temp files** -- deletes files in `TEMP_UPLOAD_PATH` older than `TEMP_MAX_AGE` (default 24 hours)

**2. Orphaned permanent files** -- scans all `TextField` values across all models, walks the upload directory, deletes files not referenced anywhere

!!! tip
    Run with `--dry-run` first to review what would be deleted. Consider adding this command to a periodic task (cron, Celery beat) for automatic maintenance.

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `CLEANUP_MEDIA` | `False` | Enable auto-cleanup on model save |
| `TEMP_UPLOAD_PATH` | `"md-editor/tmp/"` | Temp storage directory |
| `TEMP_MAX_AGE` | `86400` (24h) | Max age for temp files in seconds |
| `UPLOAD_PATH` | `"md-editor/uploads/%Y/%m/"` | Permanent storage directory |
