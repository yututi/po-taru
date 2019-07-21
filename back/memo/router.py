from rest_framework import routers
from .views import MemoViewSet

router = routers.DefaultRouter()
router.register(r'', MemoViewSet, base_name="test")
