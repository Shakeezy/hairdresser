from django.contrib import admin
from . import models

admin.site.register(models.Service)
admin.site.register(models.CloseDay)
admin.site.register(models.Appointment)
admin.site.register(models.TimeSlot)
