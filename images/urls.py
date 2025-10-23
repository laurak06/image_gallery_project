from rest_framework.routers import DefaultRouter
from .views import ImageItemViewSet

router = DefaultRouter()
router.register(r'images', ImageItemViewSet, basename='images')

urlpatterns = router.urls
