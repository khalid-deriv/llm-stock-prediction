from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, FileResponse, Http404
from django.views.decorators.http import require_POST
import os
from .forms import UploadCSVForm, UploadInstructionsForm

UPLOAD_DIR = "/tmp/llm_stock_uploads"

def ensure_user_dir(user):
    user_dir = os.path.join(UPLOAD_DIR, str(user.id))
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

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

def upload_csv(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            user_dir = ensure_user_dir(request.user)
            csv_file = request.FILES["csv_file"]
            with open(os.path.join(user_dir, "data.csv"), "wb+") as dest:
                for chunk in csv_file.chunks():
                    dest.write(chunk)
            if request.htmx:
                return HttpResponse("<div>CSV uploaded successfully.</div>")
            messages.success(request, "CSV uploaded successfully.")
            return redirect("index")
    else:
        form = UploadCSVForm()
    return render(request, "upload_csv.html", {"form": form})

def upload_instructions(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = UploadInstructionsForm(request.POST, request.FILES)
        if form.is_valid():
            user_dir = ensure_user_dir(request.user)
            md_file = request.FILES["instructions_file"]
            with open(os.path.join(user_dir, "instructions.md"), "wb+") as dest:
                for chunk in md_file.chunks():
                    dest.write(chunk)
            if request.htmx:
                return HttpResponse("<div>Instructions uploaded successfully.</div>")
            messages.success(request, "Instructions uploaded successfully.")
            return redirect("index")
    else:
        form = UploadInstructionsForm()
    return render(request, "upload_instructions.html", {"form": form})

def download_sample_csv(request):
    sample_path = os.path.join(settings.BASE_DIR, "samples", "sample_data.csv")
    if not os.path.exists(sample_path):
        raise Http404("Sample CSV not found.")
    return FileResponse(open(sample_path, "rb"), as_attachment=True, filename="sample_data.csv")

def download_sample_instructions(request):
    sample_path = os.path.join(settings.BASE_DIR, "samples", "sample_instructions.md")
    if not os.path.exists(sample_path):
        raise Http404("Sample instructions not found.")
    return FileResponse(open(sample_path, "rb"), as_attachment=True, filename="sample_instructions.md")

def download_uploaded_csv(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user_dir = ensure_user_dir(request.user)
    file_path = os.path.join(user_dir, "data.csv")
    if not os.path.exists(file_path):
        raise Http404("No uploaded CSV found.")
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename="data.csv")

def download_uploaded_instructions(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user_dir = ensure_user_dir(request.user)
    file_path = os.path.join(user_dir, "instructions.md")
    if not os.path.exists(file_path):
        raise Http404("No uploaded instructions found.")
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename="instructions.md")
