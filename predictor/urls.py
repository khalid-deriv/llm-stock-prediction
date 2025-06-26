from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("upload/csv/", views.upload_csv, name="upload_csv"),
    path("upload/instructions/", views.upload_instructions, name="upload_instructions"),
    path("download/sample-csv/", views.download_sample_csv, name="download_sample_csv"),
    path("download/sample-instructions/", views.download_sample_instructions, name="download_sample_instructions"),
    path("download/uploaded-csv/", views.download_uploaded_csv, name="download_uploaded_csv"),
    path("download/uploaded-instructions/", views.download_uploaded_instructions, name="download_uploaded_instructions"),
    path("instructions/", views.view_instructions, name="view_instructions"),
    path("predict/", views.predict_view, name="predict"),
]
