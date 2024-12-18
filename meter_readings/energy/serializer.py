from rest_framework import serializers
from .models import Customer, Meter, MeterReading

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']

class MeterSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Meter
        fields = ['id', 'serial_number', 'location', 'customer']
        
class MeterReadingSerializer(serializers.ModelSerializer):
    meter = serializers.PrimaryKeyRelatedField(queryset=Meter.objects.all())
    class Meta:
        model = MeterReading
        fields = ['id', 'meter', 'reading_value', 'timestamp']
        read_only_fields = ['id', 'timestamp']