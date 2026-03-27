from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class usersignup(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    

    
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Increased for hashed passwords
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    confirm_password = models.CharField(max_length=20)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    def is_approved(self):
        return self.status == 'approved'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class TrafficSignal(models.Model):
    SIGNAL_STATUS = [
        ('red', 'Red'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
    ]
    
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_status = models.CharField(max_length=10, choices=SIGNAL_STATUS, default='red')
    is_active = models.BooleanField(default=True)
    vehicle_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class VehicleDetection(models.Model):
    signal = models.ForeignKey(TrafficSignal, on_delete=models.CASCADE)
    vehicle_count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    lane = models.CharField(max_length=50, default='main')
    
    def __str__(self):
        return f"{self.signal.name} - {self.vehicle_count} vehicles"

class TrafficLog(models.Model):
    ALERT_LEVELS = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    signal = models.ForeignKey(TrafficSignal, on_delete=models.CASCADE)
    message = models.TextField()
    alert_level = models.CharField(max_length=10, choices=ALERT_LEVELS, default='info')
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.signal.name} - {self.alert_level}"