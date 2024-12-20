from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    
    path('', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_list, name='project_list'), 
    path('project/<int:project_id>/annotationslist', views.annotationslist, name='annotationslist'),
    path('project/<int:project_id>/image/<int:image_id>/', views.project_list, name='project_list'),
    path('createproject/',views.createproject, name='createproject'),
    path('project/<int:project_id>/addimage/', views.addimage, name='addimage'),
    path('project/<int:project_id>/createlabel/', views.createlabel, name='createlabel'),
    path('project/<int:project_id>/delete/', views.deleteproject, name='deleteproject'),
    path('project/<int:project_id>/image/<int:image_id>/delete/', views.deleteimage, name='deleteimage'),
    path('project/<int:project_id>/createlabel/<int:label_id>/delete/', views.deletelabel, name='deletelabel'),
    path('project/image/<int:image_id>/update_annotation/', views.update_annotation, name='update_annotation'),
    path('download-annotations/<int:project_id>/', views.download_annotations, name='download_annotations'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
