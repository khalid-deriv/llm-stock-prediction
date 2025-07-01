from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, FileResponse, Http404
from django.views.decorators.http import require_POST
from django.conf import settings
import os
from .forms import UploadCSVForm, UploadInstructionsForm

# Langchain imports
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI  # Default, but can be swapped for any supported LLM

import csv
import io
import re

from django.views.decorators.csrf import csrf_exempt

UPLOAD_DIR = "/tmp/llm_stock_uploads"

# Persona prompt as per spec
PERSONA_PROMPT = """
You are “The Oracle,” a world-class stock market analyst with a reputation for uncanny accuracy and deep insight. Your tone is confident, concise, and professional, but approachable. You analyze data with scientific rigor, explain your reasoning clearly, and always back up your predictions with evidence from the data. You avoid hype and speculation, focusing on actionable, data-driven insights. When presenting predictions, you rank them by expected profitability and explain the logic behind each one in plain language.

Use state of the art analysis techniques. Take into consideration:
- Technical analysis
- Fundamental analysis
- Geopolitical analysis
- News analysis

Use any data you have access to. The `data.csv` input file is a set of Stock data for an x amount of years. Use that as a baseline. Then use whatever data you have access to about current news events, geopolitical understanding, and the best fundamental & technical analysis expertise you have.
"""

def build_persona_prompt(user_instructions: str = None):
    """
    Build the full LLM prompt using the persona and user instructions.
    """
    if user_instructions:
        return f"{PERSONA_PROMPT}\n\nUser Instructions:\n{user_instructions.strip()}"
    return PERSONA_PROMPT

def get_llm():
    """
    Return a Langchain chat model instance using the API key from env.
    Uses OpenAI by default, but can be swapped for any supported LLM.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    # You can swap ChatOpenAI for any other langchain.chat_models class as needed
    return ChatOpenAI(api_key=api_key)

def call_llm_with_prompt(prompt: str, csv_data: str):
    """
    Call the LLM with the constructed prompt and CSV data.
    Returns the LLM's response.
    """
    llm = get_llm()
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", f"Here is the stock data CSV:\n\n{csv_data}\n\nPlease provide your predictions as specified.")
    ])
    messages = chat_prompt.format_messages()
    response = llm.invoke(messages)
    return response.content

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

def view_instructions(request):
    """
    Display instructions.md: user's uploaded file if present, else default sample.
    """
    if request.user.is_authenticated:
        user_dir = ensure_user_dir(request.user)
        user_md = os.path.join(user_dir, "instructions.md")
        if os.path.exists(user_md):
            with open(user_md, "r", encoding="utf-8") as f:
                content = f.read()
            return render(request, "view_instructions.html", {"instructions_md": content, "is_user": True})
    # fallback to default sample
    sample_path = os.path.join(settings.BASE_DIR, "samples", "sample_instructions.md")
    with open(sample_path, "r", encoding="utf-8") as f:
        content = f.read()
    return render(request, "view_instructions.html", {"instructions_md": content, "is_user": False})

def get_user_csv_and_instructions(request):
    """
    Returns (csv_data:str, instructions_md:str, is_user_csv:bool, is_user_md:bool)
    """
    # CSV
    user_csv = None
    user_md = None
    is_user_csv = False
    is_user_md = False
    if request.user.is_authenticated:
        user_dir = ensure_user_dir(request.user)
        csv_path = os.path.join(user_dir, "data.csv")
        md_path = os.path.join(user_dir, "instructions.md")
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                user_csv = f.read()
            is_user_csv = True
        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as f:
                user_md = f.read()
            is_user_md = True
    if not user_csv:
        # fallback to sample
        sample_csv = os.path.join(settings.BASE_DIR, "samples", "sample_data.csv")
        with open(sample_csv, "r", encoding="utf-8") as f:
            user_csv = f.read()
    if not user_md:
        sample_md = os.path.join(settings.BASE_DIR, "samples", "sample_instructions.md")
        with open(sample_md, "r", encoding="utf-8") as f:
            user_md = f.read()
    return user_csv, user_md, is_user_csv, is_user_md

def parse_llm_output(llm_output):
    """
    Parse LLM output into (prediction_csv:str, table_html:str, explanations:str)
    Expects LLM to output in a markdown-like format:
    ```csv
    symbol,month,predicted_price
    ...
    ```
    <table>...</table>
    Explanations: ...
    """
    # Extract CSV block
    csv_match = re.search(r"```csv\s*(.*?)```", llm_output, re.DOTALL)
    prediction_csv = csv_match.group(1).strip() if csv_match else ""
    # Extract HTML table (if any)
    table_match = re.search(r"(<table.*?>.*?</table>)", llm_output, re.DOTALL)
    table_html = table_match.group(1) if table_match else ""
    # Extract explanations (after "Explanation" or "Explanations")
    expl_match = re.search(r"Explanation[s]?:\s*(.*)", llm_output, re.DOTALL | re.IGNORECASE)
    explanations = expl_match.group(1).strip() if expl_match else ""
    return prediction_csv, table_html, explanations

@csrf_exempt
def predict_view(request):
    """
    View to trigger prediction using LLM.
    """
    if request.method == "POST":
        csv_data, instructions_md, is_user_csv, is_user_md = get_user_csv_and_instructions(request)
        prompt = build_persona_prompt(instructions_md)
        try:
            llm_output = call_llm_with_prompt(prompt, csv_data)
        except Exception as e:
            return render(request, "predict_result.html", {
                "error": f"LLM call failed: {e}"
            })
        prediction_csv, table_html, explanations = parse_llm_output(llm_output)
        # Validate prediction_csv: should have 120 rows (header + 119)
        csv_rows = [row for row in csv.reader(io.StringIO(prediction_csv)) if row]
        valid_csv = len(csv_rows) >= 2 and len(csv_rows) <= 121  # header + up to 120 rows
        return render(request, "predict_result.html", {
            "prediction_csv": prediction_csv,
            "table_html": table_html,
            "explanations": explanations,
            "valid_csv": valid_csv,
            "csv_rows": csv_rows,
            "error": None,
        })
    # GET: show a simple form to trigger prediction
    return render(request, "predict_form.html")
    return render(request, "predict_form.html")
