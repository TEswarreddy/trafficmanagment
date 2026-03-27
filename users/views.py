
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import usersignup
import re  # for regex


# Create your views here.

def userloginsignup(request):
    return render(request,'userloginsignup.html')


# Signup View
def signup(request):
    if request.method == 'POST':
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation: all fields filled
        if not fullname or not email or not phone or not password1 or not password2:
            messages.error(request, "All fields are required!")
            return redirect('userloginsignup')

        # Phone validation: 10 digits
        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone number must be 10 digits.")
            return redirect('userloginsignup')

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('userloginsignup')

        # Password strength validation
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('userloginsignup')
        if not re.search(r'[A-Z]', password1):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect('userloginsignup')
        if not re.search(r'[a-z]', password1):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return redirect('userloginsignup')
        if not re.search(r'[\W_]', password1):  # special char check
            messages.error(request, "Password must contain at least one special character.")
            return redirect('userloginsignup')

        # Check if email already exists
        if usersignup.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('userloginsignup')

        # Check if phone already exists
        if usersignup.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect('userloginsignup')

        # Save user
        user = usersignup(
            fullname=fullname,
            email=email,
            phone=phone,
            password=password1,
            confirm_password=password2
        )
        user.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect('userloginsignup')  # redirect to login section

    return render(request, 'userloginsignup.html')


# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if account exists
        try:
            user = usersignup.objects.get(email=email)
        except usersignup.DoesNotExist:
            messages.error(request, "Account is not created, please create an account.")
            return redirect('userloginsignup')

        # Check password
        if user.password != password:
            messages.error(request, "Invalid password.")
            return redirect('userloginsignup')
        
        if not user.is_approved():
            messages.error(request, "Your account is pending approval. Please wait for admin confirmation.")
            return redirect('userloginsignup')

        # Login success
        messages.success(request, f"Welcome {user.fullname}!")
        request.session['user_id'] = user.id  # simple session
        return redirect('dashboard')  # replace with your dashboard page

    return render(request, 'userloginsignup.html')





from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import usersignup, TrafficSignal, VehicleDetection, TrafficLog

def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first to access the dashboard.")
        return redirect('userloginsignup')

    try:
        user = usersignup.objects.get(id=user_id)
    except usersignup.DoesNotExist:
        messages.error(request, "Account not found. Please login again.")
        return redirect('userloginsignup')



    # Search functionality
    query = request.GET.get('q', '')
    
    # Get all traffic signals
    traffic_signals = TrafficSignal.objects.all()
    
    # Get vehicle detection data
    vehicle_detections = VehicleDetection.objects.all().order_by('-timestamp')[:10]
    
    # Get traffic logs
    traffic_logs = TrafficLog.objects.all().order_by('-created_at')[:20]
    
    # Get all users (for admin view)
    all_users = usersignup.objects.all().order_by('-created_at')
    
    # Statistics
    total_signals = traffic_signals.count()
    active_signals = traffic_signals.filter(is_active=True).count()
    total_vehicles_today = VehicleDetection.objects.filter(
        timestamp__date=timezone.now().date()
    ).count()
    
    # System status
    system_status = "Operational"
    critical_alerts = TrafficLog.objects.filter(alert_level='critical', resolved=False).count()
    if critical_alerts > 0:
        system_status = "Critical Alerts"
    elif active_signals < total_signals:
        system_status = "Partial Operation"

    context = {
        'user': user,
        'traffic_signals': traffic_signals,
        'vehicle_detections': vehicle_detections,
        'traffic_logs': traffic_logs,
        'all_users': all_users,
        'total_signals': total_signals,
        'active_signals': active_signals,
        'total_vehicles_today': total_vehicles_today,
        'system_status': system_status,
        'critical_alerts': critical_alerts,
        'query': query,
    }

    return render(request, 'users/dashboard.html', context)

def logout(request):
    # Clear session
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('userloginsignup')




import subprocess
import sys
from django.http import HttpResponse
import os

def run_simulation(request):
    script_path = os.path.join(os.path.dirname(__file__), "utils", "simulation.py")
    subprocess.Popen([sys.executable, script_path])
    return HttpResponse("Simulation launched")





def run_gesture_simulation(request):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Remove the extra "utils" from the path
    script_path = os.path.join(os.path.dirname(__file__), "utils", "gesturesimulation.py")

    # script_path = os.path.join(base_dir, "gesturesimulation.py")
    
    # Alternative: If the file is in users/utils/ directory
    # script_path = os.path.join(base_dir, "utils", "gesturesimulation.py")

    try:
        subprocess.Popen([sys.executable, script_path])
        return HttpResponse("Gesture simulation launched successfully")
    except Exception as e:
        return HttpResponse(f"Error launching simulation: {str(e)}")






def emergency(request):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(os.path.dirname(__file__), "emergency" ,"emergencydeep.py")

    try:
        subprocess.Popen([sys.executable, script_path])
        return HttpResponse("Emergency Mode launched successfully")
    except Exception as e:
        return HttpResponse(f"Error launching simulation: {str(e)}")            

