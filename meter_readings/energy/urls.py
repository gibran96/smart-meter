from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, MeterViewSet, MeterReadingViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'meters', MeterViewSet, basename='meter')
router.register(r'readings', MeterReadingViewSet, basename='reading')

urlpatterns = [
    path('', include(router.urls)),
]
