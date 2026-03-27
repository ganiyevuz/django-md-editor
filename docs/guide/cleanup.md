# Media Cleanup

When users upload images to the editor and later remove them from the content, the files remain in storage. The cleanup system detects and removes these orphaned files.

## Model Mixin (Automatic)

`MarkdownCleanupMixin` hooks into `save()` to compare old and new content and delete files that were removed.

```python
from django.db import models
from django_md_editor import MarkdownCleanupMixin

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
3. For each changed field, it extracts `![alt](url)` image URLs from both versions
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

The command:

1. Scans all `TextField` values across all models in the project
2. Collects every `![alt](url)` image URL that's referenced
3. Walks the upload directory (`md-editor/uploads/` by default)
4. Deletes files that aren't referenced by any model

!!! tip
    Run with `--dry-run` first to review what would be deleted. Consider adding this command to a periodic task (cron, Celery beat) for automatic maintenance.
