from celery import shared_task
from django.db.models import Avg, Sum, Count
from .models import MeterReading

@shared_task
def process_reading_async(reading_id):
    # Example: aggregate some data as a result of a new reading.
    reading = MeterReading.objects.get(id=reading_id)
    meter = reading.meter

    # For demonstration, we might compute average consumption for the meter
    avg_consumption = MeterReading.objects.filter(meter=meter).aggregate(avg=Avg('reading_value'))['avg']

    # You could store these results somewhere, send a notification, etc.
    # Here, we’ll just print as a placeholder.
    print(f"Processed reading {reading_id}. Average for meter {meter.serial_number}: {avg_consumption}")
