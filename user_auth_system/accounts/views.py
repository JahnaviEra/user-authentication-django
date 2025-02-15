from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import localtime
# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

# User Signup
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully! Please log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")
    return render(request, 'signup.html')

# Forgot Password
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            messages.success(request, "A password reset link has been sent to your email.")
        else:
            messages.error(request, "No account found with this email.")
    return render(request, 'forget_password.html')

# Change Password (Requires login)
@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')  

        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect!")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect("login")

    return render(request, 'change_password.html')

# Dashboard (Requires login)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Profile Page (Requires login)
@login_required
def profile(request):
    user = request.user

    context = {
        "user": user,
        "date_joined": localtime(user.date_joined),  # Convert to IST
        "last_login": localtime(user.last_login),    # Convert to IST
    }
    return render(request, "profile.html", context)

# Logout (Requires login)
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
