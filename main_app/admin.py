from django.contrib import admin
from .models import Care_provider, Prescription, Appointment, Photo

# Register your models here.
admin.site.register(Care_provider)
admin.site.register(Prescription)
admin.site.register(Appointment)
admin.site.register(Photo)
