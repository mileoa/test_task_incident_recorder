import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestincidentViewSet:
    def setup_method(self):
        self.client = APIClient()

    def test_create_incident(self):
        incident_data = {
            "description": "Тестовый инцидент",
            "status": "new",
            "source": "operator",
        }

        response = self.client.post(
            reverse("incidents:incident-list"),
            data=incident_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == incident_data["description"]
        assert response.data["status"] == incident_data["status"]
        assert response.data["source"] == incident_data["source"]
        assert "id" in response.data
        assert "created_at" in response.data

    def test_list_incidents(self):
        incidents_data = [
            {
                "description": "Инцидент 1",
                "status": "new",
                "source": "operator",
            },
            {
                "description": "Инцидент 2",
                "status": "in_progress",
                "source": "monitoring",
            },
            {
                "description": "Инцидент 3",
                "status": "new",
                "source": "partner",
            },
        ]

        for incident_data in incidents_data:
            self.client.post(
                reverse("incidents:incident-list"),
                data=incident_data,
                format="json",
            )

        response = self.client.get(
            reverse("incidents:incident-list"), {"status": "new"}
        )

        assert response.status_code == status.HTTP_200_OK
        new_incidents = [
            inc for inc in response.data if inc["status"] == "new"
        ]
        assert len(new_incidents) == 2

    def test_update_incident_status(self):
        create_response = self.client.post(
            reverse("incidents:incident-list"),
            data={
                "description": "Тестовый инцидент",
                "status": "new",
                "source": "operator",
            },
            format="json",
        )
        incident_id = create_response.data["id"]

        update_data = {"status": "in_progress"}
        update_response = self.client.patch(
            reverse("incidents:incident-detail", kwargs={"pk": incident_id}),
            data=update_data,
            format="json",
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["status"] == "in_progress"

    def test_update_nonexistent_incident(self):
        nonexistent_id = 99999
        update_data = {"status": "closed"}

        update_response = self.client.patch(
            reverse(
                "incidents:incident-detail", kwargs={"pk": nonexistent_id}
            ),
            data=update_data,
            format="json",
        )

        assert update_response.status_code == status.HTTP_404_NOT_FOUND

    def test_incident_validation(self):
        invalid_incidents = [
            {},  # Пустые данные
            {"description": "Без статуса"},
            {"status": "new"},
            {"source": "operator"},
        ]

        for invalid_data in invalid_incidents:
            response = self.client.post(
                reverse("incidents:incident-list"),
                data=invalid_data,
                format="json",
            )
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_incident_read_only_fields(self):
        incident_data = {
            "description": "Тестовый инцидент",
            "status": "new",
            "source": "operator",
            "id": 9999,
            "created_at": "2099-01-01T00:00:00Z",
        }

        response = self.client.post(
            reverse("incidents:incident-list"),
            data=incident_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        # Проверяем, что read-only поля не были изменены
        assert response.data["id"] != 9999
        assert "created_at" in response.data
        assert response.data["created_at"] != "2099-01-01T00:00:00Z"
