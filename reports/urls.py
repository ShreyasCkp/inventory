from django.urls import path
from . import views
from .views import stock_dashboard

urlpatterns = [
    path('rm-issuance-report/', views.rm_issuance_report, name='rm_issuance_report'),
    path('export-rm-issuance-excel/', views.export_rm_issuance_excel, name='export_rm_issuance_excel'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('export-report-excel/', views.export_report_excel, name='export_report_excel'),
    path('pm-material-issue-report/', views.pm_material_issue_report, name='pm_material_issue_report'),
    path('export-pm-material-issue-excel/', views.export_rm_issuance_excel, name='export_pm_material_issue_excel'),
    path('packing-slip-report/', views.packing_slip_report, name='packing_slip_report'),
    path('export-packing-slip-excel/', views.export_packing_slip_excel, name='export_packing_slip_excel'),
    path('fg-inward-material-report/', views.fg_inward_material_report, name='fg_inward_material_report'),
    path('export-fg-inward-material-excel/', views.export_fg_inward_material_excel, name='export_fg_inward_material_excel'),
    path('dashboard/', stock_dashboard, name='stock_dashboard'),
]
