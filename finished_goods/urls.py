from django.urls import path
from . import views
from .views import finished_inward_material_list,finished_inward_material_add,finished_inward_material_view,finished_inward_material_edit,finished_inward_material_delete
from django.contrib.auth import views as auth_views
urlpatterns = [
     # Use 'id' here
    path('inward-material/list/', views.finished_inward_material_list, name='finished_inward_material_list'),
    path('inward-material/add/', views.finished_inward_material_add, name='finished_inward_material_add'),
    path('inward-material/<int:id>/edit/', views.finished_inward_material_edit, name='finished_inward_material_edit'),  # Use 'id' here
 
    path('inward-material/<int:id>/', views.finished_inward_material_view, name='finished_inward_material_view'),
    path('inward-material/delete/<int:id>/', views.finished_inward_material_delete, name='finished_inward_material_delete'),



     path('packing-slip/create/', views.create_packing_slip, name='create_packing_slip'),
     path('packing-slip/', views.packing_slip_list, name='packing_slip_list'),

     path('view_packing_slip/<int:pk>/', views.view_packing_slip, name='view_packing_slip'),


     # path('view_packing_slip/<int:slip_id>/', views.view_packing_slip, name='view_packing_slip'),
     path('packing-slip/edit/<int:pk>/', views.edit_packing_slip, name='edit_packing_slip'),
     path('packing-slip/delete/<int:pk>/', views.delete_packing_slip, name='delete_packing_slip'),


     path('fg-label/create/', views.create_fg_label, name='create_fg_label'),
     path('fg-label/', views.fg_label_list, name='fg_label_list'),
     path('fg-label/edit/<int:pk>/', views.edit_fg_label, name='edit_fg_label'),
     path('fg-label/delete/<int:pk>/', views.delete_fg_label, name='delete_fg_label'),
     path('print-fg-label/<int:pk>/', views.print_fg_label, name='print_fg_label'),
     path('view/<int:pk>/', views.fg_label_details, name='fg_label_details'),  # ✅ Add this view


  
 ]


