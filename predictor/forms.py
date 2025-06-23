from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV", required=True)

class UploadInstructionsForm(forms.Form):
    instructions_file = forms.FileField(label="Upload instructions.md", required=True)
