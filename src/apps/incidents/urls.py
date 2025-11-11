from rest_framework import routers

from .views import IncidentViewSet

app_name = "incidents"
router = routers.DefaultRouter()
router = routers.DefaultRouter()

router.register(r"incidents", IncidentViewSet, basename="incident")

urlpatterns = [
    *router.urls,
]
