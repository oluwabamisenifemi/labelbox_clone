from django import forms
from .models import Annotation,Project, Image,Label



class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ['label']
        widgets = {
            'label': forms.Select(attrs={
                'class': 'form-control',  # Bootstrap class for styling
                'placeholder': 'Select a label',
            }),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap class for styling
                'placeholder': 'Enter project name',  # Placeholder text
            }),
        }





class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_file']
        widgets = {
            'image_file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',  # Bootstrap class for file inputs
                'accept': 'image/*',  # Limit upload to image files
            }),
        }



class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap styling
                'placeholder': 'Enter label name',  # Placeholder text
            }),
        }




