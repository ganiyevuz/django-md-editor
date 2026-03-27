# Management Commands

## `cleanup_markdown_media`

Finds and deletes orphaned media files that were uploaded through the markdown editor but are no longer referenced in any model's `TextField`.

### Usage

```bash
# Preview orphaned files without deleting
python manage.py cleanup_markdown_media --dry-run

# Delete orphaned files
python manage.py cleanup_markdown_media
```

### Options

| Flag | Description |
|------|-------------|
| `--dry-run` | List orphaned files without deleting them |

### How It Works

1. Iterates over all registered Django models
2. Reads every `TextField` value and extracts `![alt](url)` image URLs
3. Walks the upload directory tree (default: `md-editor/uploads/`)
4. Compares stored files against referenced URLs
5. Deletes (or lists) files that aren't referenced anywhere

### Example Output

```
$ python manage.py cleanup_markdown_media --dry-run
  [dry-run] Would delete: md-editor/uploads/2026/01/1706000000_old-image.png
  [dry-run] Would delete: md-editor/uploads/2026/02/1709000000_unused.jpg

Would delete 2 orphaned file(s).
```

### Scheduling

Consider running this periodically via cron or a task scheduler:

```bash
# Crontab: run weekly on Sunday at 3 AM
0 3 * * 0 cd /path/to/project && python manage.py cleanup_markdown_media
```
