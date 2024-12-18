from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from meter_readings.energy.serializer import CustomerSerializer, MeterSerializer, MeterReadingSerializer
from .models import Customer, Meter, MeterReading
from rest_framework import status
from .tasks import process_reading_async

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class MeterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Meter.objects.all()
    serializer_class = MeterSerializer

class MeterReadingViewSet(viewsets.ModelViewSet):
    queryset = MeterReading.objects.all().order_by('-timestamp')
    serializer_class = MeterReadingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reading = serializer.save()
        
        # Trigger async processing
        process_reading_async.delay(reading.id)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
