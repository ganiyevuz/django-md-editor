from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase, override_settings


class UploadViewTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user("testuser", password="testpass")

    @patch("django_markdown_widget.views.load_upload_handler")
    def test_successful_upload(self, mock_load):
        mock_handler = mock_load.return_value
        mock_handler.save.return_value = "/media/uploads/test.png"

        self.client.login(username="testuser", password="testpass")
        with open(__file__, "rb") as f:
            response = self.client.post(
                "/md-editor/upload",
                {"file": f},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "/media/uploads/test.png"

    def test_no_file_returns_400(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/md-editor/upload")
        assert response.status_code == 400

    def test_unauthenticated_rejected_by_default(self):
        response = self.client.post("/md-editor/upload")
        assert response.status_code == 401

    @override_settings(MD_EDITOR={"REQUIRE_AUTH": False})
    def test_unauthenticated_allowed_when_auth_disabled(self):
        response = self.client.post("/md-editor/upload")
        assert response.status_code == 400  # no file, but auth passed

    @patch("django_markdown_widget.views.load_upload_handler")
    def test_validation_error_returns_400(self, mock_load):
        mock_handler = mock_load.return_value
        mock_handler.validate.side_effect = ValidationError("Bad file")

        self.client.login(username="testuser", password="testpass")
        with open(__file__, "rb") as f:
            response = self.client.post(
                "/md-editor/upload",
                {"file": f},
            )
        assert response.status_code == 400
        assert "Bad file" in response.json()["error"]

    def test_get_not_allowed(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/md-editor/upload")
        assert response.status_code == 405
