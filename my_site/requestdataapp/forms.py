from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField(label='Full name', max_length=100)
    age = forms.IntegerField(label='Your Age', min_value="1", max_value="99")
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Biography'}))


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('Virus detected!')
    
    
class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name], widget=forms.FileInput(attrs={'class': 'form-control'}))