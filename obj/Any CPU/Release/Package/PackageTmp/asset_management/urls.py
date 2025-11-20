from django.urls import path
from . import views 


urlpatterns = [
   

    # Inward Material URLs
    path('am_inward-material/list/', views.am_inward_material_list, name='am_inward_material_list'),
    path('am_inward-material/add/', views.am_inward_material_add, name='am_inward_material_add'),
    path('am_inward-material/<int:id>/edit/', views.am_inward_material_edit, name='am_inward_material_edit'),
    path('am_inward-material/<int:id>/', views.am_inward_material_view, name='am_inward_material_view'),
    path('am_inward-material/delete/<int:id>/', views.am_inward_material_delete, name='am_inward_material_delete'),

    # Asset Material Issue URLs
    path('asset-material-issue/list/', views.asset_material_issue_list, name='asset_material_issue_list'),
    path('asset-material-issue/add/', views.asset_material_issue_add, name='asset_material_issue_add'),
    path('asset-material-issue/<int:id>/edit/', views.asset_material_issue_edit, name='asset_material_issue_edit'),
    path('asset-material-issue/<int:id>/', views.asset_material_issue_view, name='asset_material_issue_view'),
    path('asset-material-issue/delete/<int:id>/', views.asset_material_issue_delete, name='asset_material_issue_delete'),
]
