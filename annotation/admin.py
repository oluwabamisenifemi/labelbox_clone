from django.contrib import admin
from .models import  Image, Annotation,Project, Image,Label
from django.contrib import admin



admin.site.register(Annotation)
admin.site.register(Project)
admin.site.register(Image)
admin.site.register(Label)
