from django.db import models
from django.urls import reverse
from urllib.parse import quote

class Customer(models.Model):
    STATUS = [("active","Active"),("inactive","Inactive"),("prospect","Prospect")]
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="active")
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("customer_detail", args=[self.pk])

    @property
    def whatsapp_link(self):
        number = "".join(c for c in self.phone if c.isdigit())
        return f"https://wa.me/{number}?text={quote('Hello ' + self.name)}" if number else "#"

    def __str__(self):
        return self.name

class Lead(models.Model):
    STAGES = [
        ("new","New"),("contacted","Contacted"),("qualified","Qualified"),
        ("proposal","Proposal"),("won","Won"),("lost","Lost")
    ]
    title = models.CharField(max_length=180)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="leads")
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stage = models.CharField(max_length=20, choices=STAGES, default="new")
    source = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Invoice(models.Model):
    STATUS = [("draft","Draft"),("sent","Sent"),("paid","Paid"),("overdue","Overdue")]
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="draft")
    due_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.amount + self.tax

    def __str__(self):
        return self.invoice_number
