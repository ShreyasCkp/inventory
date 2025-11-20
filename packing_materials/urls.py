from django.urls import path
from . import views
from .views import (
    packing_material_list, packing_material_add, packing_material_view,
    packing_material_edit, packing_material_delete, get_items,
    pm_material_issue_list, pm_material_issue_add, pm_material_issue_edit,
    pm_material_issue_view, pm_material_issue_delete,pm_label_view
)
from .views import purchase_order_detail, edit_file, delete_file

urlpatterns = [
    path('pm-label/create/', views.create_pm_label, name='create_pm_label'),
    path('view/<int:pk>/', pm_label_view, name='view_pm_label'),  # Correct path pattern
    path('pm-label/', views.pm_label_list, name='pm_label_list'),
    path('pm-label/edit/<int:pk>/', views.edit_pm_label, name='edit_pm_label'),
    path('pm-label/delete/<int:pk>/', views.delete_pm_label, name='delete_pm_label'),
    path('print-pm-label/<int:pk>/', views.print_pm_label, name='print_pm_label'),

    path('packing-material/list/', packing_material_list, name='packing_material_list'),
    path('packing-material/add/', packing_material_add, name='packing_material_add'),
    path('packing-material/<int:id>/edit/', packing_material_edit, name='packing_material_edit'),
    path('packing-material/<int:id>/', packing_material_view, name='packing_material_view'),
    path('packing-material/delete/<int:id>/', packing_material_delete, name='packing_material_delete'),
    path('get-items/', get_items, name='get-items'),
 # PM Material Issue URLs
    path('packing-materials/list/', pm_material_issue_list, name='pm_material_issue_list'),
    path('packing-materials/add/', pm_material_issue_add, name='pm_material_issue_add'),
    path('packing-materials/edit/<int:matIssueId>/', pm_material_issue_edit, name='pm_material_issue_edit'),
    path('packing-materials/view/<int:matIssueId>/', pm_material_issue_view, name='pm_material_issue_view'),
    path('packing-materials/delete/<int:matIssueId>/', pm_material_issue_delete, name='pm_material_issue_delete'),

    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase-orders/<int:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase-orders/new/', views.purchase_order_create, name='purchase_order_create'),
    path('purchase-orders/<int:pk>/edit/', views.purchase_order_edit, name='purchase_order_edit'),
    path('purchase-orders/<int:pk>/delete/', views.purchase_order_delete, name='purchase_order_delete'),


    path('edit_file/<int:pk>/', edit_file, name='edit_file'),
    path('delete_file/<int:pk>/', delete_file, name='delete_file'),
   
   path('save_uploaded_files/', views.save_uploaded_files, name='save_uploaded_files'),
]
