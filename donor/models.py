from django.db import models

class Donor(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    last_donation = models.DateField(null=True, blank=True)
    gender = models.CharField(
    max_length=10,
    choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
)


    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class BloodStock(models.Model):
    blood_group = models.CharField(max_length=3, unique=True)
    units = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.blood_group}: {self.units} units"


class BloodRequest(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.blood_group} ({self.status})"
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"