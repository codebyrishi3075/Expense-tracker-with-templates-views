from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random

from .models import EmailOTP, User


# ---------------- HOME PAGE ----------------

def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, "account/home.html")


# ---------------- OTP GENERATOR ----------------

def generate_otp():
    return str(random.randint(100000, 999999))


# ---------------- REGISTER ----------------

def register_user(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username", "").strip()
            email    = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()

            if not username:
                return JsonResponse({"success": False, "message": "Username is required"}, status=400)
            if not email:
                return JsonResponse({"success": False, "message": "Email is required"}, status=400)
            if not password:
                return JsonResponse({"success": False, "message": "Password is required"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "message": "Email already exists"}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({"success": False, "message": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            otp = generate_otp()
            EmailOTP.objects.filter(user=user, purpose="register").delete()
            EmailOTP.objects.create(user=user, otp=otp, purpose="register")

            try:
                send_mail(
                    subject="Verify your Email",
                    message=f"Your OTP is {otp}",
                    from_email=None,
                    recipient_list=[user.email],
                )
            except Exception as e:
                print(f"Email send error: {e}")
                return JsonResponse({"success": False, "message": "Failed to send OTP"}, status=500)

            return JsonResponse({"success": True, "message": "OTP sent to your email"})

        return render(request, "account/register.html")

    except Exception as e:
        print(f"Registration error: {e}")
        return JsonResponse({"success": False, "message": "Registration failed."}, status=500)


# ---------------- VERIFY EMAIL OTP ----------------

def verify_email_otp(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email", "").strip()
            otp   = request.POST.get("otp", "").strip()

            if not email:
                return JsonResponse({"success": False, "message": "Email is required"}, status=400)
            if not otp:
                return JsonResponse({"success": False, "message": "OTP is required"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"success": False, "message": "Invalid email"}, status=404)

            otp_obj = EmailOTP.objects.filter(user=user, otp=otp, purpose="register", is_used=False).last()
            if not otp_obj:
                return JsonResponse({"success": False, "message": "Invalid OTP"}, status=400)
            if otp_obj.is_expired():
                return JsonResponse({"success": False, "message": "OTP expired"}, status=400)

            otp_obj.is_used = True
            otp_obj.save()

            user.is_active = True
            user.is_email_verified = True
            user.save()

            return JsonResponse({"success": True, "message": "Email verified successfully"})

        return render(request, "account/verify_otp.html")

    except Exception as e:
        print(f"OTP verification error: {e}")
        return JsonResponse({"success": False, "message": "Verification failed"}, status=500)


# ---------------- LOGIN ----------------

def login_user(request):
    try:
        if request.method == "POST":
            email    = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()

            if not email:
                return JsonResponse({"success": False, "message": "Email is required"}, status=400)
            if not password:
                return JsonResponse({"success": False, "message": "Password is required"}, status=400)

            user = authenticate(username=email, password=password)

            if not user:
                return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)
            if not user.is_email_verified:
                return JsonResponse({"success": False, "message": "Email not verified."}, status=401)

            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful"})

        return render(request, "account/login.html")

    except Exception as e:
        print(f"Login error: {e}")
        return JsonResponse({"success": False, "message": "Login failed"}, status=500)


# ---------------- LOGOUT ----------------
# FIXED: redirect to home instead of JSON response

@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


# ---------------- PROFILE ----------------

@login_required
def profile(request):
    context = {
        "id":            request.user.id,
        "full_name":     f"{request.user.first_name} {request.user.last_name}".strip(),
        "email":         request.user.email,
        "username":      request.user.username,
        "profile_image": request.user.profile_image,
    }
    return render(request, "account/profile.html", context)


# ---------------- UPDATE PROFILE ----------------

@login_required
def update_profile(request):
    try:
        if request.method == "POST":
            first_name = request.POST.get("first_name", "").strip()
            last_name  = request.POST.get("last_name", "").strip()

            if not first_name and not last_name:
                return JsonResponse({"success": False, "message": "At least one field is required"}, status=400)

            request.user.first_name = first_name
            request.user.last_name  = last_name
            request.user.save()

            return JsonResponse({"success": True, "message": "Profile updated successfully"})

        return render(request, "account/update_profile.html")

    except Exception as e:
        print(f"Profile update error: {e}")
        return JsonResponse({"success": False, "message": "Profile update failed"}, status=500)


# ---------------- UPLOAD AVATAR ----------------

@login_required
def upload_avatar(request):
    try:
        if request.method == "POST":
            file = request.FILES.get("profile_image")

            if not file:
                return JsonResponse({"success": False, "message": "No file selected"}, status=400)

            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if file.content_type not in allowed_types:
                return JsonResponse({"success": False, "message": "Only image files are allowed"}, status=400)

            if file.size > 5 * 1024 * 1024:
                return JsonResponse({"success": False, "message": "File size should be less than 5MB"}, status=400)

            request.user.profile_image = file
            request.user.save()

            return JsonResponse({"success": True, "message": "Profile image updated successfully"})

        return render(request, "account/upload_avatar.html")

    except Exception as e:
        print(f"Avatar upload error: {e}")
        return JsonResponse({"success": False, "message": "Upload failed"}, status=500)


# ---------------- PASSWORD RESET REQUEST ----------------

def password_reset_request(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email", "").strip()

            if not email:
                return JsonResponse({"success": False, "message": "Email is required"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"success": False, "message": "User not found"}, status=404)

            otp = generate_otp()
            EmailOTP.objects.filter(user=user, purpose="reset").delete()
            EmailOTP.objects.create(user=user, otp=otp, purpose="reset")

            try:
                send_mail(
                    subject="Password Reset OTP",
                    message=f"Your OTP is {otp}",
                    from_email=None,
                    recipient_list=[user.email],
                )
            except Exception as e:
                print(f"Email send error: {e}")
                return JsonResponse({"success": False, "message": "Failed to send OTP"}, status=500)

            return JsonResponse({"success": True, "message": "OTP sent to your email"})

        return render(request, "account/password_reset_request.html")

    except Exception as e:
        print(f"Password reset request error: {e}")
        return JsonResponse({"success": False, "message": "Request failed"}, status=500)


# ---------------- VERIFY RESET OTP ----------------

def password_reset_verify_otp(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email", "").strip()
            otp   = request.POST.get("otp", "").strip()

            if not email:
                return JsonResponse({"success": False, "message": "Email is required"}, status=400)
            if not otp:
                return JsonResponse({"success": False, "message": "OTP is required"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"success": False, "message": "Invalid email"}, status=404)

            otp_obj = EmailOTP.objects.filter(user=user, otp=otp, purpose="reset", is_used=False).last()
            if not otp_obj:
                return JsonResponse({"success": False, "message": "Invalid OTP"}, status=400)
            if otp_obj.is_expired():
                return JsonResponse({"success": False, "message": "OTP expired"}, status=400)

            otp_obj.is_used = True
            otp_obj.save()

            return JsonResponse({"success": True, "message": "OTP verified"})

        return render(request, "account/password_reset_verify.html")

    except Exception as e:
        print(f"OTP verify error: {e}")
        return JsonResponse({"success": False, "message": "Verification failed"}, status=500)


# ---------------- RESET PASSWORD ----------------

def password_reset_confirm(request):
    try:
        if request.method == "POST":
            email        = request.POST.get("email", "").strip()
            new_password = request.POST.get("new_password", "").strip()

            if not email:
                return JsonResponse({"success": False, "message": "Email is required"}, status=400)
            if not new_password:
                return JsonResponse({"success": False, "message": "Password is required"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"success": False, "message": "Invalid email"}, status=404)

            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return JsonResponse({"success": False, "message": " ".join(e.messages)}, status=400)

            user.set_password(new_password)
            user.save()

            return JsonResponse({"success": True, "message": "Password reset successfully"})

        return render(request, "account/password_reset_confirm.html")

    except Exception as e:
        print(f"Password reset confirm error: {e}")
        return JsonResponse({"success": False, "message": "Password reset failed"}, status=500)