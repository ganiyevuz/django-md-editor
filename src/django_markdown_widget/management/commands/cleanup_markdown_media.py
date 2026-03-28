from __future__ import annotations

import time

from django.apps import apps
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db.models import TextField

from django_markdown_widget.cleanup import _url_to_storage_path, extract_media_urls
from django_markdown_widget.settings import get_setting


class Command(BaseCommand):
    help = "Find and delete orphaned media files and expired temp uploads."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List orphaned files without deleting them.",
        )

    def handle(self, **options):
        dry_run = options["dry_run"]
        deleted_count = 0

        # 1. Clean expired temp uploads
        deleted_count += self._clean_temp_uploads(dry_run)

        # 2. Clean orphaned permanent uploads
        deleted_count += self._clean_orphaned_uploads(dry_run)

        if deleted_count == 0:
            self.stdout.write(self.style.SUCCESS("No orphaned files found."))

    def _clean_temp_uploads(self, dry_run: bool) -> int:
        temp_prefix = get_setting("TEMP_UPLOAD_PATH")
        max_age = get_setting("TEMP_MAX_AGE")
        now = time.time()

        try:
            expired = self._find_expired_temps(temp_prefix, now, max_age)
        except FileNotFoundError:
            return 0

        for path in expired:
            if dry_run:
                self.stdout.write(f"  [dry-run] Would delete temp: {path}")
            else:
                default_storage.delete(path)
                self.stdout.write(f"  Deleted temp: {path}")

        if expired:
            label = "Would delete" if dry_run else "Deleted"
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n{label} {len(expired)} expired temp file(s)."
                )
            )
        return len(expired)

    def _find_expired_temps(
        self, prefix: str, now: float, max_age: int
    ) -> list[str]:
        expired = []
        try:
            dirs, files = default_storage.listdir(prefix)
        except FileNotFoundError:
            return expired

        for filename in files:
            full_path = prefix + filename
            try:
                modified = default_storage.get_modified_time(full_path)
                age = now - modified.timestamp()
                if age > max_age:
                    expired.append(full_path)
            except (OSError, NotImplementedError):
                expired.append(full_path)

        for dirname in dirs:
            expired.extend(
                self._find_expired_temps(prefix + dirname + "/", now, max_age)
            )
        return expired

    def _clean_orphaned_uploads(self, dry_run: bool) -> int:
        upload_prefix = get_setting("UPLOAD_PATH").split("%")[0]

        referenced_paths = set()
        for model in apps.get_models():
            text_fields = [
                f.name
                for f in model._meta.get_fields()
                if isinstance(f, TextField)
            ]
            if not text_fields:
                continue

            for obj in model.objects.only(*text_fields).iterator():
                for field_name in text_fields:
                    text = getattr(obj, field_name, "") or ""
                    for url in extract_media_urls(text):
                        path = _url_to_storage_path(url)
                        if path:
                            referenced_paths.add(path)

        try:
            orphaned = self._find_orphans(upload_prefix, referenced_paths)
        except FileNotFoundError:
            return 0

        for path in orphaned:
            if dry_run:
                self.stdout.write(f"  [dry-run] Would delete: {path}")
            else:
                default_storage.delete(path)
                self.stdout.write(f"  Deleted: {path}")

        if orphaned:
            label = "Would delete" if dry_run else "Deleted"
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n{label} {len(orphaned)} orphaned file(s)."
                )
            )
        return len(orphaned)

    def _find_orphans(
        self, prefix: str, referenced: set[str]
    ) -> list[str]:
        orphaned = []
        try:
            dirs, files = default_storage.listdir(prefix)
        except FileNotFoundError:
            return orphaned

        for filename in files:
            full_path = prefix + filename
            if full_path not in referenced:
                orphaned.append(full_path)

        for dirname in dirs:
            orphaned.extend(
                self._find_orphans(prefix + dirname + "/", referenced)
            )
        return orphaned
