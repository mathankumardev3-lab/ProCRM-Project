from django import forms
from .models import Customer, Lead, Invoice

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name","company","email","phone","status","address","notes"]
        widgets = {"address":forms.Textarea(attrs={"rows":2}),"notes":forms.Textarea(attrs={"rows":3})}

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["title","customer","value","stage","source","notes"]
        widgets = {"notes":forms.Textarea(attrs={"rows":3})}

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["invoice_number","customer","amount","tax","status","due_date","description"]
        widgets = {"due_date":forms.DateInput(attrs={"type":"date"}),"description":forms.Textarea(attrs={"rows":3})}
