from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password,check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def home(request):
    print(request.user)
    print(request.user.is_authenticated)

    return render(request, "home.html")


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        hashed_password = make_password(password)

        try:
            validate_email(email)
        except ValidationError:
            return redirect({
                "error": "Enter a valid email address"
            }, status=400)

        if User.objects.filter(email=email).exists():
            return redirect({
                "error": "Email already registered"
            }, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password= hashed_password
        )

        return redirect("login")

    return render(request, "register.html")


def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        

        user = authenticate(
            username=username,
            password=password
        )
        

        if user is not None:
            if check_password(password,user.password):
                login(request, user)
                return redirect("home")          

        return render(
            request,
            "login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "login.html")

def logout_user(request):
    logout(request)

    return redirect("home")