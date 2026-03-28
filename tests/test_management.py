from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.db.models import TextField
from django.test import TestCase


STORAGE_PATH = (
    "django_markdown_widget.management.commands.cleanup_markdown_media.default_storage"
)
APPS_PATH = (
    "django_markdown_widget.management.commands.cleanup_markdown_media.apps"
)


class CleanupMarkdownMediaTests(TestCase):
    @patch(STORAGE_PATH)
    @patch(APPS_PATH)
    def test_dry_run_lists_without_deleting(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []
        # temp dir empty, uploads have orphan
        def listdir_side_effect(path):
            if path == "md-editor/tmp/":
                return [], []
            if path == "md-editor/uploads/":
                return [], ["orphan.png"]
            return [], []

        mock_storage.listdir.side_effect = listdir_side_effect

        out = StringIO()
        call_command("cleanup_markdown_media", "--dry-run", stdout=out)

        output = out.getvalue()
        assert "dry-run" in output
        assert "orphan.png" in output
        mock_storage.delete.assert_not_called()

    @patch(STORAGE_PATH)
    @patch(APPS_PATH)
    def test_deletes_orphaned_files(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []

        def listdir_side_effect(path):
            if path == "md-editor/tmp/":
                return [], []
            if path == "md-editor/uploads/":
                return [], ["orphan.png"]
            return [], []

        mock_storage.listdir.side_effect = listdir_side_effect

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        output = out.getvalue()
        assert "Deleted" in output
        mock_storage.delete.assert_called_once()

    @patch(STORAGE_PATH)
    @patch(APPS_PATH)
    def test_no_orphans_found(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []
        mock_storage.listdir.return_value = ([], [])

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        assert "No orphaned files" in out.getvalue()

    @patch(STORAGE_PATH)
    @patch(APPS_PATH)
    def test_handles_missing_upload_directory(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []
        mock_storage.listdir.side_effect = FileNotFoundError

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        assert "No orphaned files" in out.getvalue()

    @patch(STORAGE_PATH)
    @patch(APPS_PATH)
    def test_keeps_referenced_files(self, mock_apps, mock_storage):
        field = TextField()
        field.name = "content"
        mock_model = MagicMock()
        mock_model._meta.get_fields.return_value = [field]

        mock_obj = MagicMock()
        mock_obj.content = "![img](/media/md-editor/uploads/2026/03/keep.png)"
        mock_model.objects.only.return_value.iterator.return_value = [mock_obj]

        mock_apps.get_models.return_value = [mock_model]

        def listdir_side_effect(path):
            if path == "md-editor/tmp/":
                return [], []
            if path == "md-editor/uploads/":
                return ["2026"], []
            if path == "md-editor/uploads/2026/":
                return ["03"], []
            if path == "md-editor/uploads/2026/03/":
                return [], ["keep.png"]
            return [], []

        mock_storage.listdir.side_effect = listdir_side_effect

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        assert "No orphaned files" in out.getvalue()
        mock_storage.delete.assert_not_called()

    @patch(STORAGE_PATH)
    @patch(APPS_PATH)
    def test_deletes_expired_temp_files(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []

        def listdir_side_effect(path):
            if path == "md-editor/tmp/":
                return [], ["old_file.png"]
            if path == "md-editor/uploads/":
                return [], []
            return [], []

        mock_storage.listdir.side_effect = listdir_side_effect

        # File modified 48 hours ago (expired)
        from datetime import datetime, timezone
        old_time = datetime.fromtimestamp(0, tz=timezone.utc)
        mock_storage.get_modified_time.return_value = old_time

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        output = out.getvalue()
        assert "temp" in output.lower()
        mock_storage.delete.assert_called_once()
