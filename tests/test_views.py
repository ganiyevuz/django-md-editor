import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings


class PreviewViewTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user("testuser", password="testpass")

    def test_post_returns_rendered_html(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            "/md-editor/preview/",
            data=json.dumps({"text": "**bold**"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "html" in data

    def test_get_not_allowed(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/md-editor/preview/")
        assert response.status_code == 405

    def test_unauthenticated_rejected_by_default(self):
        response = self.client.post(
            "/md-editor/preview/",
            data=json.dumps({"text": "test"}),
            content_type="application/json",
        )
        assert response.status_code == 403

    @override_settings(MD_EDITOR={"REQUIRE_AUTH": False})
    def test_unauthenticated_allowed_when_auth_disabled(self):
        response = self.client.post(
            "/md-editor/preview/",
            data=json.dumps({"text": "**bold**"}),
            content_type="application/json",
        )
        assert response.status_code == 200

    def test_empty_text_returns_empty_html(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            "/md-editor/preview/",
            data=json.dumps({"text": ""}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["html"] == ""


class UploadViewTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User.objects.create_user("testuser", password="testpass")

    @patch("django_md_editor.views.load_upload_handler")
    def test_successful_upload(self, mock_load):
        mock_handler = mock_load.return_value
        mock_handler.save.return_value = "/media/uploads/test.png"

        self.client.login(username="testuser", password="testpass")
        with open(__file__, "rb") as f:
            response = self.client.post(
                "/md-editor/upload/",
                {"file": f},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "/media/uploads/test.png"

    def test_no_file_returns_400(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/md-editor/upload/")
        assert response.status_code == 400

    def test_unauthenticated_rejected_by_default(self):
        response = self.client.post("/md-editor/upload/")
        assert response.status_code == 403

    def test_get_not_allowed(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/md-editor/upload/")
        assert response.status_code == 405
