from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse

def index(request):
    return render(request, "base.html")

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.htmx:
                return HttpResponse("<script>window.location.reload()</script>")
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.htmx:
                return HttpResponse("<script>window.location.reload()</script>")
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    if request.htmx:
        return HttpResponse("<script>window.location.reload()</script>")
    return redirect("index")
