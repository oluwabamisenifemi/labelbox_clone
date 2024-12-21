from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Image(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    description = models.TextField(default="No description provided.") 

    def __str__(self):
        return f"Image in {self.project.name}"
    def clean(self):
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif']
        if not any(self.image_file.name.lower().endswith(ext) for ext in allowed_extensions):
            raise ValidationError("Unsupported file format. Please upload a valid image.")
        
    def save(self, *args, **kwargs):
       
        super().save(*args, **kwargs)
        
       
        if self.image_file:
            img = PILImage.open(self.image_file)
            
            
            img.thumbnail((300, 300))

          
            thumb_io = BytesIO()

            
            img.save(thumb_io, format='JPEG', quality=85)
            
           
            thumb_name = self.image_file.name.split('.')[0] + '_thumb.jpg'  # You may choose a different name if necessary
            self.image_file.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)

       
        super().save(*args, **kwargs)
       


class Annotation(models.Model):
    image = models.ForeignKey(Image, related_name='annotations', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)

    def clean(self):
      
        if not self.label:
            raise ValidationError("Label cannot be empty.")

        
        if not Label.objects.filter(project=self.image.project, name=self.label).exists():
            raise ValidationError(f"The label '{self.label}' is not valid for the project '{self.image.project.name}'.")

    def save(self, *args, **kwargs):
        '''self.clean()'''  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Annotation for {self.image.id}: {self.label}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['image'], name='unique_annotation_per_image')
        ]


class Label(models.Model):
    project = models.ForeignKey(Project, related_name='labels', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)