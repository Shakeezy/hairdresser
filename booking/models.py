from django.db import models
import uuid

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_es = models.CharField(max_length=100, unique=True, null=True)
    price = models.FloatField()
    duration = models.DurationField()

    def __str__(self):
        return f'{self.name} - {self.price}€'

class CloseDay(models.Model):
    date = models.DateField(unique=True)
    motive = models.CharField(blank=False, null=False)
    def __str__(self):
        return f'{self.date} - {self.motive}'

class TimeSlot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    class Meta:
        unique_together = ('date', 'time')
    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')} {self.time.strftime('%H:%M')}"

class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    client_name = models.CharField(blank=False, null=False, max_length=50)
    client_last_name = models.CharField(blank=False, null=False, max_length=50)
    phone_number = models.CharField(blank=False, null=False, max_length=15)
    email = models.EmailField(blank=False, null=False)
    cancel_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return (
            f"Appointment for {self.client_name} {self.client_last_name} "
            f"on {self.slot.date.strftime('%d/%m/%Y')} at {self.slot.time.strftime('%H:%M')} - "
            f"Service: {self.service.name} - Phone: {self.phone_number}"
        )
