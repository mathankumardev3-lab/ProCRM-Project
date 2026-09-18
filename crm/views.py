from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Lead, Invoice
from .forms import CustomerForm, LeadForm, InvoiceForm

@login_required
def dashboard(request):
    context = {
        "customers_count": Customer.objects.count(),
        "leads_count": Lead.objects.count(),
        "invoices_count": Invoice.objects.count(),
        "revenue": Invoice.objects.filter(status="paid").aggregate(v=Sum("amount"))["v"] or 0,
        "pipeline": Lead.objects.exclude(stage="lost").aggregate(v=Sum("value"))["v"] or 0,
        "recent_customers": Customer.objects.order_by("-created_at")[:5],
        "recent_leads": Lead.objects.select_related("customer").order_by("-created_at")[:5],
    }
    return render(request, "dashboard.html", context)

@login_required
def customer_list(request):
    q = request.GET.get("q","")
    customers = Customer.objects.filter(Q(name__icontains=q)|Q(company__icontains=q)|Q(email__icontains=q)).order_by("-created_at")
    return render(request, "customers/list.html", {"customers":customers,"q":q})

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request,"Customer created successfully."); return redirect("customer_list")
    return render(request,"form.html",{"form":form,"title":"Add Customer","back":"customer_list"})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer,pk=pk)
    return render(request,"customers/detail.html",{"customer":customer})

@login_required
def customer_edit(request, pk):
    obj=get_object_or_404(Customer,pk=pk); form=CustomerForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,"Customer updated."); return redirect("customer_detail",pk=pk)
    return render(request,"form.html",{"form":form,"title":"Edit Customer","back":"customer_list"})

@login_required
def customer_delete(request, pk):
    obj=get_object_or_404(Customer,pk=pk)
    if request.method=="POST": obj.delete(); messages.success(request,"Customer deleted.")
    return redirect("customer_list")

@login_required
def lead_list(request):
    q=request.GET.get("q","")
    leads=Lead.objects.select_related("customer").filter(Q(title__icontains=q)|Q(customer__name__icontains=q)).order_by("-created_at")
    return render(request,"leads/list.html",{"leads":leads,"q":q})

@login_required
def lead_create(request):
    form=LeadForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,"Lead created."); return redirect("lead_list")
    return render(request,"form.html",{"form":form,"title":"Add Lead","back":"lead_list"})

@login_required
def lead_edit(request,pk):
    obj=get_object_or_404(Lead,pk=pk); form=LeadForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,"Lead updated."); return redirect("lead_list")
    return render(request,"form.html",{"form":form,"title":"Edit Lead","back":"lead_list"})

@login_required
def lead_delete(request,pk):
    obj=get_object_or_404(Lead,pk=pk)
    if request.method=="POST": obj.delete(); messages.success(request,"Lead deleted.")
    return redirect("lead_list")

@login_required
def invoice_list(request):
    q=request.GET.get("q","")
    invoices=Invoice.objects.select_related("customer").filter(Q(invoice_number__icontains=q)|Q(customer__name__icontains=q)).order_by("-created_at")
    return render(request,"invoices/list.html",{"invoices":invoices,"q":q})

@login_required
def invoice_create(request):
    form=InvoiceForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,"Invoice created."); return redirect("invoice_list")
    return render(request,"form.html",{"form":form,"title":"Add Invoice","back":"invoice_list"})

@login_required
def invoice_edit(request,pk):
    obj=get_object_or_404(Invoice,pk=pk); form=InvoiceForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,"Invoice updated."); return redirect("invoice_list")
    return render(request,"form.html",{"form":form,"title":"Edit Invoice","back":"invoice_list"})

@login_required
def invoice_delete(request,pk):
    obj=get_object_or_404(Invoice,pk=pk)
    if request.method=="POST": obj.delete(); messages.success(request,"Invoice deleted.")
    return redirect("invoice_list")
