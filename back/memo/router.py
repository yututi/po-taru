from rest_framework import routers
from .views import MemoViewSet

router = routers.SimpleRouter()
router.register(r'memo', MemoViewSet, base_name="memo")
