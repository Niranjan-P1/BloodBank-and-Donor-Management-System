from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Donor, BloodStock, BloodRequest
from .forms import DonorForm, BloodStockForm, BloodRequestForm, ContactForm
# For PDF export
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from datetime import datetime
from django.utils.dateparse import parse_date
# ============================
# Home Page
# ============================
def home(request):
    donors = Donor.objects.all()
    blood_stock = BloodStock.objects.all()
    blood_requests = BloodRequest.objects.order_by('-requested_at')[:5]  # Latest 5 requests

    # --- Search & Filter Logic ---
    search_name = request.GET.get("name")
    filter_blood = request.GET.get("blood_group")
    filter_city = request.GET.get("city")

    if search_name:
        donors = donors.filter(name__icontains=search_name)
    if filter_blood:
        donors = donors.filter(blood_group__iexact=filter_blood)
    if filter_city:
        donors = donors.filter(city__icontains=filter_city)

    blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

    total_donors = donors.count()
    total_groups = len(blood_groups)
    total_requests = BloodRequest.objects.count()

    return render(
        request,
        "donor/home.html",
        {
            "donors": donors,
            "blood_stock": blood_stock,
            "blood_requests": blood_requests,
            "blood_groups": blood_groups,
            "total_donors": total_donors,
            "total_groups": total_groups,
            "total_requests": total_requests,
        },
    )

# ============================
# Register Donor
# ============================
def register_donor(request):
    if request.method == "POST":
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Donor registered successfully!")
            return redirect("home")
    else:
        form = DonorForm()
    return render(request, "donor/register_donor.html", {"form": form})

# ============================
# Blood Request
# ============================
def blood_request(request):
    if request.method == "POST":
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()  # status defaults to "Pending"
            messages.success(request, "Your blood request has been submitted!")
            return redirect("blood_request")  # 👈 redirect back to this page
    else:
        form = BloodRequestForm()

    # Fetch all previous requests (latest first)
    blood_requests = BloodRequest.objects.order_by("-requested_at")

    return render(
        request,
        "donor/request_blood.html",
        {"form": form, "blood_requests": blood_requests}
    )


# ============================
# Reports Page (with filters)
# ============================
def reports_page(request):
    return render(request, "donor/report.html")

# ============================
# PDF Export (filtered + sections)
# ============================
def export_filtered_report_pdf(request):
    donors = Donor.objects.all()
    blood_stock = BloodStock.objects.all()
    blood_requests = BloodRequest.objects.all()

    # ✅ Get filters
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        if start and end:
            blood_requests = blood_requests.filter(requested_at__date__range=[start, end])

    # ✅ Section checkboxes
    include_donors = request.GET.get("include_donors")
    include_stock = request.GET.get("include_stock")
    include_requests = request.GET.get("include_requests")

    template = get_template('filtered_report_pdf.html')
    html = template.render({
        'donors': donors if include_donors else None,
        'blood_stock': blood_stock if include_stock else None,
        'blood_requests': blood_requests if include_requests else None,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bloodbank_filtered_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF")
    return response


# ============================
# About Page
# ============================
def about(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect("about")
    else:
        form = ContactForm()
    return render(request, "donor/about.html", {"form": form})

def reports_page(request):
    return render(request, "donor/report.html")
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import BloodRequest

# Only staff/admin allowed
def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def manage_requests(request):
    requests_list = BloodRequest.objects.all().order_by("-id")

    if request.method == "POST":
        req_id = request.POST.get("request_id")
        action = request.POST.get("action")

        blood_req = get_object_or_404(BloodRequest, id=req_id)

        if action == "approve":
            blood_req.status = "Approved"
        elif action == "reject":
            blood_req.status = "Rejected"

        blood_req.save()
        return redirect("manage_requests")  # reload page after update

    return render(request, "donor/manage_requests.html", {"requests": requests_list})


