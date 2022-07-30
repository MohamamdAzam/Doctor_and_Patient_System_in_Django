from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Medical)
admin.site.register(Hospital)
admin.site.register(Appointment)
admin.site.register(Hospital_Appointment)
admin.site.register(Adminstration)
admin.site.register(Prescription)
admin.site.register(Billing_Record)
admin.site.register(Medical_Record)
