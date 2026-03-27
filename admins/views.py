from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages

# Cloud Kitchen Admin Credentials
CLOUD_KITCHEN_ADMIN_EMAIL = "admin@gmail.com"
CLOUD_KITCHEN_ADMIN_PASSWORD = "admin"


def admin_login(request):
    return render(request,'admin_login.html')

def admin_login_check(request):
    """Admin login for Cloud Kitchen - Email & Password only"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == CLOUD_KITCHEN_ADMIN_EMAIL and password == CLOUD_KITCHEN_ADMIN_PASSWORD:
            request.session["admin_logged_in"] = True
            messages.success(request, "Welcome to  Admin Panel!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid email or password!")

    return render(request, "admin_login.html")

from users.models import usersignup

def admin_logout(request):
    """Logout admin"""
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("basefunction")


def admin_dashboard(request):
    # Get all users for the users table
    all_users = usersignup.objects.all().order_by('-created_at')

    context = {
        "all_users": all_users,
    }

    return render(request, "admins/admin_dashboard.html", context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from users.models import usersignup

def activate_user(request, user_id):
    """Activate a user account"""
    user = get_object_or_404(usersignup, id=user_id)
    user.status = 'approved'
    user.save()
    messages.success(request, f"User {user.fullname} has been activated successfully!")
    return redirect('admin_dashboard')

def block_user(request, user_id):
    """Block a user account"""
    user = get_object_or_404(usersignup, id=user_id)
    user.status = 'rejected'
    user.save()
    messages.success(request, f"User {user.fullname} has been blocked!")
    return redirect('admin_dashboard')

def delete_user(request, user_id):
    """Delete a user account"""
    user = get_object_or_404(usersignup, id=user_id)
    user_name = user.fullname
    user.delete()
    messages.success(request, f"User {user_name} has been deleted successfully!")
    return redirect('admin_dashboard')

def view_user_details(request, user_id):
    """View detailed information about a user"""
    user = get_object_or_404(usersignup, id=user_id)
    
    context = {
        'user': user,
    }
    return render(request, 'admins/user_details.html', context)