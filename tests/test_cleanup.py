from unittest.mock import patch

from django.test import TestCase

from django_markdown_widget.cleanup import (
    _url_to_storage_path,
    delete_orphaned_media,
    extract_media_urls,
)


class ExtractMediaUrlsTests(TestCase):
    def test_extracts_single_image(self):
        text = "Hello ![alt](/media/md-editor/uploads/2026/03/img.png)"
        assert extract_media_urls(text) == {"/media/md-editor/uploads/2026/03/img.png"}

    def test_extracts_multiple_images(self):
        text = (
            "![a](/media/md-editor/uploads/2026/03/a.png)\n"
            "![b](/media/md-editor/uploads/2026/03/b.jpg)"
        )
        urls = extract_media_urls(text)
        assert len(urls) == 2

    def test_ignores_regular_links(self):
        text = "Check [this link](https://example.com)"
        assert extract_media_urls(text) == set()

    def test_empty_text(self):
        assert extract_media_urls("") == set()
        assert extract_media_urls(None) == set()

    def test_deduplicates_same_url(self):
        text = (
            "![a](/media/md-editor/uploads/2026/03/img.png)\n"
            "![b](/media/md-editor/uploads/2026/03/img.png)"
        )
        assert len(extract_media_urls(text)) == 1


class UrlToStoragePathTests(TestCase):
    def test_converts_media_url_to_path(self):
        url = "/media/md-editor/uploads/2026/03/1234_test.png"
        result = _url_to_storage_path(url)
        assert result == "md-editor/uploads/2026/03/1234_test.png"

    def test_returns_none_for_external_url(self):
        url = "https://example.com/image.png"
        assert _url_to_storage_path(url) is None

    def test_returns_none_for_unrelated_path(self):
        url = "/static/css/style.css"
        assert _url_to_storage_path(url) is None


class DeleteOrphanedMediaTests(TestCase):
    @patch("django_markdown_widget.cleanup.default_storage")
    def test_deletes_removed_image(self, mock_storage):
        mock_storage.exists.return_value = True

        old = "![img](/media/md-editor/uploads/2026/03/1234_old.png)"
        new = "Text without images"

        deleted = delete_orphaned_media(old, new)

        assert len(deleted) == 1
        mock_storage.delete.assert_called_once()

    @patch("django_markdown_widget.cleanup.default_storage")
    def test_keeps_image_still_referenced(self, mock_storage):
        img = "![img](/media/md-editor/uploads/2026/03/1234_keep.png)"
        old = f"Before {img}"
        new = f"After {img}"

        deleted = delete_orphaned_media(old, new)

        assert deleted == []
        mock_storage.delete.assert_not_called()

    @patch("django_markdown_widget.cleanup.default_storage")
    def test_skips_nonexistent_file(self, mock_storage):
        mock_storage.exists.return_value = False

        old = "![img](/media/md-editor/uploads/2026/03/1234_gone.png)"
        new = ""

        deleted = delete_orphaned_media(old, new)

        assert deleted == []
        mock_storage.delete.assert_not_called()

    @patch("django_markdown_widget.cleanup.default_storage")
    def test_handles_multiple_removals(self, mock_storage):
        mock_storage.exists.return_value = True

        old = (
            "![a](/media/md-editor/uploads/2026/03/a.png)\n"
            "![b](/media/md-editor/uploads/2026/03/b.png)\n"
            "![c](/media/md-editor/uploads/2026/03/c.png)"
        )
        new = "![b](/media/md-editor/uploads/2026/03/b.png)"

        deleted = delete_orphaned_media(old, new)

        assert len(deleted) == 2
        assert mock_storage.delete.call_count == 2

    def test_empty_old_text(self):
        deleted = delete_orphaned_media("", "![img](/media/img.png)")
        assert deleted == []

    def test_both_empty(self):
        deleted = delete_orphaned_media("", "")
        assert deleted == []
