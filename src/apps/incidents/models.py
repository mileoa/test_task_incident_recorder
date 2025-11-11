from django.db import models


class Incident(models.Model):
    description = models.CharField(max_length=40000)
    status = models.CharField(
        max_length=50,
        choices=[
            ("new", "Новый"),
            ("in_progress", "В работе"),
            ("solution_given", "Решение предоставлено"),
            ("closed", "Закрыт"),
        ],
    )
    source = models.CharField(
        max_length=50,
        choices=[
            ("operator", "Оператор"),
            ("monitoring", "Система мониторинга"),
            ("partner", "Заказчик"),
        ],
    )
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]

    def __str__(self):
        return f"{self.description[:20]} - {self.created_at}"
