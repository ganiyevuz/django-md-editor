from django.test import TestCase, override_settings

from django_markdown_widget.settings import get_setting


class GetSettingTests(TestCase):
    def test_returns_default_renderer_class(self):
        result = get_setting("RENDERER_CLASS")
        assert result == "django_markdown_widget.renderers.DefaultRenderer"

    def test_returns_default_upload_handler_class(self):
        result = get_setting("UPLOAD_HANDLER_CLASS")
        assert result == "django_markdown_widget.uploads.DefaultUploadHandler"

    def test_returns_default_toolbar(self):
        result = get_setting("TOOLBAR")
        assert "bold" in result
        assert "heading" in result
        assert "separator" in result

    def test_returns_default_max_upload_size(self):
        result = get_setting("MAX_UPLOAD_SIZE")
        assert result == 50 * 1024 * 1024

    def test_returns_default_allowed_upload_types(self):
        result = get_setting("ALLOWED_UPLOAD_TYPES")
        assert "image/png" in result
        assert "image/jpeg" in result

    def test_returns_default_upload_path(self):
        result = get_setting("UPLOAD_PATH")
        assert result == "md-editor/uploads/%Y/%m/"

    def test_returns_default_height(self):
        result = get_setting("DEFAULT_HEIGHT")
        assert result == "300px"

    def test_returns_default_placeholder(self):
        result = get_setting("PLACEHOLDER")
        assert result == "Add your comment here..."

    def test_returns_default_require_auth(self):
        result = get_setting("REQUIRE_AUTH")
        assert result is True

    @override_settings(MD_EDITOR={"MAX_UPLOAD_SIZE": 5 * 1024 * 1024})
    def test_user_override_respected(self):
        result = get_setting("MAX_UPLOAD_SIZE")
        assert result == 5 * 1024 * 1024

    @override_settings(MD_EDITOR={"MAX_UPLOAD_SIZE": 5 * 1024 * 1024})
    def test_non_overridden_settings_keep_defaults(self):
        result = get_setting("RENDERER_CLASS")
        assert result == "django_markdown_widget.renderers.DefaultRenderer"

    def test_unknown_key_raises_key_error(self):
        with self.assertRaises(KeyError):
            get_setting("NONEXISTENT_KEY")
