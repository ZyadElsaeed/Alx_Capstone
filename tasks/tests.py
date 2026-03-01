from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Task


class TaskCreateTests(APITestCase):
    """Tests for creating tasks."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="strongpass123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_task_success(self):
        data = {"title": "Test Task", "description": "A test task"}
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Task")
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(response.data["user"], "testuser")

    def test_create_task_without_title(self):
        data = {"description": "Missing title"}
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_unauthenticated(self):
        self.client.credentials()  # remove auth
        data = {"title": "Test Task"}
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskPermissionTests(APITestCase):
    """Tests to verify users can only access their own tasks."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="strongpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="strongpass123"
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        self.task = Task.objects.create(
            title="User1 Task",
            description="Belongs to user1",
            user=self.user1,
        )

    def test_owner_can_view_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "User1 Task")

    def test_non_owner_cannot_view_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_owner_cannot_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/", {"title": "Hacked"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_owner_cannot_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_list_shows_only_own_tasks(self):
        Task.objects.create(title="User2 Task", user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [t["title"] for t in response.data["results"]]
        self.assertIn("User1 Task", titles)
        self.assertNotIn("User2 Task", titles)


class TaskFilterSearchTests(APITestCase):
    """Tests for filtering and searching tasks."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="strongpass123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        Task.objects.create(title="Buy groceries", status="pending", user=self.user)
        Task.objects.create(title="Clean house", status="completed", user=self.user)
        Task.objects.create(title="Buy gifts", status="completed", user=self.user)

    def test_filter_by_status(self):
        response = self.client.get("/api/tasks/?status=completed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_search_by_title(self):
        response = self.client.get("/api/tasks/?search=Buy")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
