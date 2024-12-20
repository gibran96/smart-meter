from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.name
    
class Meter(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, related_name='meters', on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"Meter {self.serial_number} (Customer: {self.customer.name})"

class MeterReading(models.Model):
    meter = models.ForeignKey(Meter, related_name='readings', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reading_value = models.FloatField()

    def __str__(self) -> str:
        return f"Reading: {self.reading_value} at {self.timestamp} for {self.meter.serial_number}"