from django.urls import path
from . import views
from .views import category_list,category_add,category_edit,category_delete,category_detail,company_form,item_list,item_add,item_edit,item_delete,item_detail
from django.contrib.auth import views as auth_views
from .views import get_user_location
from .views import forgot_password_view


urlpatterns = [
     path('', views.home_view, name='home'),  # Home page
  path('login/', views.login_view, name='login'),  # Login page
  path('get-user-location/', get_user_location, name='get_user_location'),
   path('logout/', views.logout_view, name='logout'),
  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout
   path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('vendors/', views.vendor_list, name='vendor_list'),  # Vendor list
    path('vendors/add/', views.vendor_add, name='vendor_add'),  # Add vendor
    path('vendors/edit/<int:pk>/', views.vendor_edit, name='vendor_edit'),  # Edit vendor
    path('vendors/delete/<int:pk>/', views.vendor_delete, name='vendor_delete'),  # Delete vendor
    path('vendors/detail/<int:pk>/', views.vendor_detail, name='vendor_detail'),  # View vendor details
     path('categories/', category_list, name='category_list'),  # List categories
    path('categories/add/', category_add, name='category_add'),  # Add category
    path('categories/edit/<int:pk>/', category_edit, name='category_edit'),  # Edit category
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),  # Delete category
    path('categories/detail/<int:pk>/', category_detail, name='category_detail'), 
    path('customer/', views.customer_list, name='customer_list'),  # Customer List Page
    path('customers/add/', views.customer_add, name='customer_add'),  # Add customer
    path('customers/edit/<int:pk>/', views.customer_edit, name='customer_edit'),  # Edit customer
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),  # Delete customer
    path('customers/view/<int:pk>/', views.customer_view, name='customer_view'),  # View Details  
    path('company-form/', company_form, name='company_form'),

     path('item/', views.item_list, name='item_list'),  # Item List Page
     path('items/add/', views.item_add, name='item_add'),  # Add Item
    path('items/edit/<int:pk>/', views.item_edit, name='item_edit'),  # Edit Item
    path('items/delete/<int:pk>/', views.item_delete, name='item_delete'),  # Delete Item
    path('items/view/<int:pk>/', views.item_detail, name='item_detail'),  # View Item Details  


   path('store/', views.store_list, name='store_list'),  # Display store
   path('store/add/', views.store_add, name='store_add'),  # Add store
   path('store/edit/<int:pk>/', views.store_edit, name='store_edit'),  # Edit store
   path('store/delete/<int:pk>/', views.store_delete, name='store_delete'),  # Delete store
     # Add this for viewing details
   path('store/view/<int:pk>/', views.store_view, name='store_view'),  # View Details  

       #Bag_Boxes
   path('bag_boxes/', views.bag_boxes_list, name='bag_boxes_list'),  # Display bag_boxes
   path('bag_boxes/add/', views.bag_boxes_add, name='bag_boxes_add'),  # Add bag_boxes         #/*   Bag_Boxes        bag_boxes  *     /
   path('bag_boxes/edit/<int:pk>/', views.bag_boxes_edit, name='bag_boxes_edit'),  # Edit bag_boxes
   path('bag_boxes/delete/<int:pk>/', views.bag_boxes_delete, name='bag_boxes_delete'),  # Delete bag_boxes
     # Add this for viewing details
   path('bag_boxes/view/<int:pk>/', views.bag_boxes_view, name='bag_boxes_view'),  # View Details 


     
 

]
