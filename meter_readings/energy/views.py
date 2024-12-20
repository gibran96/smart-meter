from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from meter_readings.energy.serializer import CustomerSerializer, MeterSerializer, MeterReadingSerializer
from .models import Customer, Meter, MeterReading
from rest_framework import status
from .tasks import fetch_user_meter_usage_async
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import redis

r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class MeterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Meter.objects.all()
    serializer_class = MeterSerializer

class MeterReadingViewSet(viewsets.ModelViewSet):
    queryset = MeterReading.objects.all().order_by('-timestamp')
    serializer_class = MeterReadingSerializer

@api_view(['POST'])
def start_user_usage_task(request, user_id):
    """
    POST /api/usage/<user_id>/start
    Starts the Celery task to fetch and process the user's usage data.
    """
    fetch_user_meter_usage_async.delay(user_id)
    return Response({"message": "Task started"}, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def get_user_usage_data(request, user_id):
    """
    GET /api/usage/<user_id>/data
    Fetches processed meter data for the user from Redis.
    If no data is found, assumes processing is still underway.
    """
    cached_data = r.get(f"user_{user_id}_data")
    if cached_data is None:
        return Response({"status": "processing"}, status=status.HTTP_202_ACCEPTED)
    data = json.loads(cached_data)
    return Response(data, status=status.HTTP_200_OK)