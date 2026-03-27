from __future__ import annotations

from django.apps import apps
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db.models import TextField

from django_md_editor.cleanup import _url_to_storage_path, extract_media_urls
from django_md_editor.settings import get_setting


class Command(BaseCommand):
    help = "Find and delete orphaned media files uploaded via the markdown editor."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List orphaned files without deleting them.",
        )

    def handle(self, **options):
        dry_run = options["dry_run"]
        upload_prefix = get_setting("UPLOAD_PATH").split("%")[0]

        # Collect all media URLs referenced in any TextField across the project
        referenced_paths = set()
        for model in apps.get_models():
            text_fields = [
                f.name for f in model._meta.get_fields() if isinstance(f, TextField)
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

        # List files in upload directory and find orphans
        try:
            dirs, files = default_storage.listdir(upload_prefix)
        except FileNotFoundError:
            self.stdout.write("No upload directory found. Nothing to clean up.")
            return

        orphaned = self._find_orphans(upload_prefix, referenced_paths)

        if not orphaned:
            self.stdout.write(self.style.SUCCESS("No orphaned files found."))
            return

        for path in orphaned:
            if dry_run:
                self.stdout.write(f"  [dry-run] Would delete: {path}")
            else:
                default_storage.delete(path)
                self.stdout.write(f"  Deleted: {path}")

        label = "Would delete" if dry_run else "Deleted"
        self.stdout.write(
            self.style.SUCCESS(f"\n{label} {len(orphaned)} orphaned file(s).")
        )

    def _find_orphans(self, prefix: str, referenced: set[str]) -> list[str]:
        """Recursively walk storage under prefix, return unreferenced paths."""
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
            orphaned.extend(self._find_orphans(prefix + dirname + "/", referenced))
        return orphaned
