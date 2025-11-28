from django.contrib import admin
from .models import Donor, BloodStock, BloodRequest
from .models import ContactMessage

admin.site.register(ContactMessage)
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "city", "contact", "last_donation")

@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ("blood_group", "units")

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "city", "status", "requested_at")
    list_filter = ("status", "blood_group")

    def save_model(self, request, obj, form, change):
        """Update stock when request is approved"""
        if change:  # if editing existing request
            old_obj = BloodRequest.objects.get(pk=obj.pk)
            # Only update if status changes to Approved
            if old_obj.status != "Approved" and obj.status == "Approved":
                try:
                    stock = BloodStock.objects.get(blood_group=obj.blood_group)
                    if stock.units > 0:
                        stock.units -= 1
                        stock.save()
                except BloodStock.DoesNotExist:
                    pass
        super().save_model(request, obj, form, change)
