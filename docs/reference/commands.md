# Management Commands

## `cleanup_markdown_media`

Finds and deletes orphaned media files and expired temp uploads.

### Usage

```bash
# Preview what would be deleted
python manage.py cleanup_markdown_media --dry-run

# Delete orphaned files
python manage.py cleanup_markdown_media
```

### Options

| Flag | Description |
|------|-------------|
| `--dry-run` | List files without deleting them |

### How It Works

The command runs two cleanup phases:

**Phase 1: Expired temp files**

- Walks the `TEMP_UPLOAD_PATH` directory (`md-editor/tmp/`)
- Deletes files older than `TEMP_MAX_AGE` (default 24 hours)
- These are files uploaded during editing but never finalized (user abandoned the form)

**Phase 2: Orphaned permanent files**

- Scans every `TextField` across all Django models
- Extracts media URLs from markdown content (images, videos, links, embeds)
- Walks the `UPLOAD_PATH` directory tree
- Deletes files not referenced by any model

### Example Output

```
$ python manage.py cleanup_markdown_media --dry-run
  [dry-run] Would delete temp: md-editor/tmp/1706000000_abandoned.png

Would delete 1 expired temp file(s).
  [dry-run] Would delete: md-editor/uploads/2026/01/1706000000_old-image.png

Would delete 1 orphaned file(s).
```

### Scheduling

```bash
# Crontab: run daily at 3 AM
0 3 * * * cd /path/to/project && python manage.py cleanup_markdown_media
```
