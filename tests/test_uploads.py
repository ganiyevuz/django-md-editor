from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from django_markdown_widget.uploads import BaseUploadHandler, DefaultUploadHandler


class BaseUploadHandlerTests(TestCase):
    def test_cannot_instantiate_abstract_class(self):
        with self.assertRaises(TypeError):
            BaseUploadHandler()


class DefaultUploadHandlerTests(TestCase):
    def test_validate_accepts_allowed_type(self):
        handler = DefaultUploadHandler()
        file = SimpleUploadedFile("test.png", b"fake-png", content_type="image/png")
        handler.validate(file)  # Should not raise

    def test_validate_rejects_disallowed_type(self):
        handler = DefaultUploadHandler()
        file = SimpleUploadedFile(
            "test.exe", b"fake-exe", content_type="application/exe"
        )
        with self.assertRaises(ValidationError) as ctx:
            handler.validate(file)
        assert "File type" in str(ctx.exception)

    @override_settings(MD_EDITOR={"MAX_UPLOAD_SIZE": 100})
    def test_validate_rejects_oversized_file(self):
        handler = DefaultUploadHandler()
        content = b"x" * 200
        file = SimpleUploadedFile("big.png", content, content_type="image/png")
        with self.assertRaises(ValidationError) as ctx:
            handler.validate(file)
        assert "File size" in str(ctx.exception)

    @patch("django_markdown_widget.uploads.default_storage")
    def test_save_stores_file_and_returns_url(self, mock_storage):
        mock_storage.save.return_value = "md-editor/uploads/2026/03/test.png"
        mock_storage.url.return_value = "/media/md-editor/uploads/2026/03/test.png"

        handler = DefaultUploadHandler()
        file = SimpleUploadedFile("test.png", b"fake-png", content_type="image/png")
        url = handler.save(file)

        assert url == "/media/md-editor/uploads/2026/03/test.png"
        mock_storage.save.assert_called_once()
