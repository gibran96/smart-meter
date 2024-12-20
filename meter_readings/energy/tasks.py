from celery import shared_task
from django.db.models import Avg, Sum, Count
from .models import MeterReading
from .models import Customer, MeterReading, Meter
from django.utils import timezone
import random
import json
import redis

r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

@shared_task
def fetch_user_meter_usage_async(user_id):
    """
    Fetch and process meter readings for a given user and store the results in Redis.
    """
    try:
        customer = Customer.objects.get(id=user_id)
    except Customer.DoesNotExist:
        # If user doesn't exist, store an error message in Redis
        error_data = {"error": "Customer not found"}
        r.set(f"user_{user_id}_data", json.dumps(error_data))
        return

    readings = MeterReading.objects.filter(meter__customer=customer).order_by('timestamp')
    if not readings.exists():
        data = {
            "user_id": user_id,
            "name": customer.name,
            "average_usage": 0,
            "total_usage": 0,
            "readings": []
        }
    else:
        avg_val = readings.aggregate(avg=Avg('reading_value'))['avg']
        total_val = readings.aggregate(total=Sum('reading_value'))['total']
        timeseries = [
            {"timestamp": r.timestamp.isoformat(), "value": r.reading_value}
            for r in readings
        ]
        data = {
            "user_id": user_id,
            "name": customer.name,
            "average_usage": avg_val,
            "total_usage": total_val,
            "readings": timeseries
        }

    # Store the data in Redis as a JSON string
    r.set(f"user_{user_id}_data", json.dumps(data))

@shared_task
def add_hourly_readings():
    # For each customer, for each meter, insert a new reading that increments over time
    customers = Customer.objects.all()
    for customer in customers:
        for meter in customer.meters.all():
            # Get the last reading for this meter
            last_reading = meter.readings.order_by('-timestamp').first()

            if last_reading:
                # Start from the last reading value
                current_value = last_reading.reading_value
            else:
                # If no reading exists, start from 0
                current_value = 0.0

            # Simulate the consumption increment in the last minute
            # For example, increment by a random amount between 0.1 and 2 units
            increment = random.uniform(0.1, 2.0)
            new_reading_value = current_value + increment

            MeterReading.objects.create(
                meter=meter,
                reading_value=new_reading_value,
                timestamp=timezone.now()
            )

    print("Minute readings added with incremental values")
