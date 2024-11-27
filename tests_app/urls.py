from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import RegisterView
from .views import BloodTestCreateView, BloodTestListView, BloodTestStatsView, BatchUploadView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/tests/', BloodTestCreateView.as_view(), name='create-test'),
    path('api/tests/list/', BloodTestListView.as_view(), name='list-tests'),
    path('api/tests/stats/', BloodTestStatsView.as_view(), name='test-stats'),
    path('api/tests/upload/', BatchUploadView.as_view(), name='batch-upload'),
]
