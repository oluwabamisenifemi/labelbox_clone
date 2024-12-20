from django import forms
from .models import Annotation,Project, Image,Label

class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ['label']  

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', ]


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_file']


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']



