from django.urls import path
import rest_framework
import rest_framework.routers

from .views import TrainingSessionViewSet

router = rest_framework.routers.SimpleRouter()
router.register(r'training_session', TrainingSessionViewSet)

urlpatterns = router.urls