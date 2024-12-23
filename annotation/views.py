from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Image, Annotation,Label
from .forms import AnnotationForm, ProjectForm,ImageForm,AnnotationForm,LabelForm
from django.contrib import messages
import json
from django.http import HttpResponse

from .models import Project



def project_list(request, project_id=None):
    projects = Project.objects.all()
    selected_project = None
    images = []

    if project_id:
        selected_project = get_object_or_404(Project, id=project_id)
        images = selected_project.images.all()

    return render(request, 'annotation/project_list.html', {
        'projects': projects,
        'selected_project': selected_project,
        'images': images
    })




def addimage(request, project_id):
   
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
       
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            
            image = image_form.save(commit=False)
            image.project = project 
            image.save()
           

    else:
        image_form = ImageForm()  

    return render(request, 'annotation/addimage.html', {
        'project': project,
        'image_form': image_form
    })



def annotationslist(request, project_id):
    
    selected_project = get_object_or_404(Project, id=project_id)
    
   
    annotations = Annotation.objects.filter(image__project=selected_project)
    
    return render(request, 'annotation/annotationslist.html', {
        'annotations': annotations,
        'project': selected_project,
    })



def createlabel(request, project_id):
    labels = []
    if project_id:
        selected_project = get_object_or_404(Project, id=project_id)
        labels = selected_project.labels.all()


    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        label_form = LabelForm(request.POST, request.FILES)
        if label_form.is_valid():
            Label = label_form.save(commit=False)
            Label.project = project 
            Label.save()
            '''return redirect('project_list', project_id=project.id)'''
    else:
        label_form = LabelForm()

    return render(request, 'annotation/createlabel.html', {
        'project': project,
        'label_form': label_form,
        'labels':labels
    })


def deletelabel(request, project_id, label_id):
    label = get_object_or_404(Label, id=label_id, project_id=project_id)
    label.delete()  
    messages.success(request, f"Project '{Label.name}' has been deleted.")
    return redirect('createlabel', project_id=project_id )  



def createproject(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
           
            project = project_form.save()

            messages.success(request, 'Project has been created successfully!')
            return redirect('project_list')  
        else:
            messages.error(request, 'There was an error with the form submission. Please check the details and try again.')
    else:
        project_form = ProjectForm()

    return render(request, 'annotation/createproject.html', {
        'project_form': project_form,
    })

def deleteproject(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()  
    messages.success(request, f"Project '{project.name}' has been deleted.")
    return redirect('project_list')  

def deleteimage(request, project_id, image_id):
    
    image = get_object_or_404(Image, id=image_id, project_id=project_id)
    image.delete()
    
    return redirect('project_list', project_id=project_id)









from django.core.exceptions import ValidationError


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Annotation, Label

def update_annotation(request, image_id):
  
    image = get_object_or_404(Image, id=image_id)

    if request.method == "POST":
        
        annotation_label = request.POST.get('annotation_label', '').strip()

        
        if not annotation_label:
            messages.error(request, "Label cannot be empty.")
            return redirect('project_list', project_id=image.project.id)

       
        valid_labels = Label.objects.filter(project=image.project).values_list('name', flat=True)
        if annotation_label not in valid_labels:
            messages.error(request, f"Invalid label: '{annotation_label}' for the project.")
            

      
        annotation, created = Annotation.objects.get_or_create(image=image)
        annotation.label = annotation_label
        try:
            annotation.save()
            if created:
                messages.success(request, "Annotation created successfully.")
            else:
                messages.success(request, "Annotation updated successfully.")
        except ValidationError as e:
            messages.error(request, f"Error saving annotation: {e.messages[0]}")
            
     
        """return redirect('project_list', project_id=image.project.id)"""

    
    messages.error(request, "Invalid request method.")
    return redirect('project_list', project_id=image.project.id)








def download_annotations(request, project_id):
 
    project = get_object_or_404(Project, id=project_id)

    
    annotations = {
        "project": project.name,
        "annotations": [
            {
                "data": {"image_url": image.image_file.url},
                "annotation": [{"label": annotation.label} for annotation in image.annotations.all()]  
            }
            for image in project.images.all()
            if image.annotations.exists()  
        ]
    }

    
    if not annotations["annotations"]:
        return redirect('project_list', project_id=project_id)

 
    json_content = json.dumps(annotations, indent=4)

   
    response = HttpResponse(json_content, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{project.name.replace(" ", "_")}_annotations.json"'
    return response
