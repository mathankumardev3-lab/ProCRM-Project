from django.contrib import admin
from .models import Customer, Lead, Invoice
admin.site.register(Customer)
admin.site.register(Lead)
admin.site.register(Invoice)
