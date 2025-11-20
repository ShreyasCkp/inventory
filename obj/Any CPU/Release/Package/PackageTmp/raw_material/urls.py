from django.urls import path
from . import views
from .views import inward_material_list,inward_material_add,inward_material_view,inward_material_edit,inward_material_delete
from django.contrib.auth import views as auth_views
from .views import rm_material_issue_list,rm_material_issue_add,rm_material_issue_edit
from .views import rm_material_issue_list, rm_material_issue_add, rm_material_issue_edit, rm_material_issue_delete
import raw_material.views

from .views import rm_label_list,edit_rm_label,delete_rm_label,print_rm_label,rm_label_view

urlpatterns = [
     # Use 'id' here
    path('inward-material/list/', views.inward_material_list, name='inward_material_list'),
    path('inward-material/add/', views.inward_material_add, name='inward_material_add'),
    path('inward-material/<int:id>/edit/', views.inward_material_edit, name='inward_material_edit'),  # Use 'id' here
 
    path('inward-material/<int:id>/', views.inward_material_view, name='inward_material_view'),
    path('inward-material/delete/<int:id>/', views.inward_material_delete, name='inward_material_delete'),

  
 


    # List View
    path('rm-material-issue/list/', views.rm_material_issue_list, name='rm_material_issue_list'),
    
    # Add View
    path('rm-material-issue/add/', views.rm_material_issue_add, name='rm_material_issue_add'),
    
    # Edit View
    path('rm-material-issue/<int:id>/edit/', views.rm_material_issue_edit, name='rm_material_issue_edit'),
    
    # View Details
    path('rm-material-issue/<int:id>/', views.rm_material_issue_view, name='rm_material_issue_view'),
    
    # Delete
    path('rm-material-issue/delete/<int:id>/', views.rm_material_issue_delete, name='rm_material_issue_delete'),



    path('rm-label/create/', views.create_rm_label, name='create_rm_label'),
    path('rm-label/', views.rm_label_list, name='rm_label_list'),
    path('rm-label/edit/<int:pk>/', views.edit_rm_label, name='edit_rm_label'),
    path('rm-label/delete/<int:pk>/', views.delete_rm_label, name='delete_rm_label'),
    path('print-rm-label/<int:pk>/', views.print_rm_label, name='print_rm_label'),
    path('rm-label/view/<int:pk>/', views.rm_label_view, name='view_rm_label'),

]

