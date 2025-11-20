from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import connection  # Import connection for raw SQL queries
from .models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login



def user_list(request):
    """Display all users with options to add, edit, and delete."""
    users = User.objects.all()
    return render(request, 'Administrator_settings/user_list.html', {'users': users})

def user_add(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, city_name FROM location")
        locations_list = cursor.fetchall()

    locations = [{'id': row[0], 'name': row[1]} for row in locations_list]  # Fix here

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Replace ID with city_name manually (if needed)
            selected_id = request.POST.get("location")
            selected_location = next((l["name"] for l in locations if str(l["id"]) == selected_id), None)
            form.instance.location = selected_location  # Save name, not ID
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()

    return render(request, 'Administrator_settings/user_form.html', {'form': form, 'title': 'Add User', 'locations': locations})

def user_edit(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, city_name FROM location")
        locations_list = cursor.fetchall()

    locations = [{'id': row[0], 'name': row[1]} for row in locations_list]

    user_instance = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_instance)
        if form.is_valid():
            # Replace ID with city_name manually
            selected_id = request.POST.get("location")
            selected_location = next((l["name"] for l in locations if str(l["id"]) == selected_id), None)
            form.instance.location = selected_location
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user_instance)

    return render(request, 'Administrator_settings/user_form.html', {
        'form': form,
        'title': 'Edit User',
        'locations': locations
    })



def user_delete(request, pk):
    """Delete a vendor."""
    vendor = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('user_list')
    
    return render(request, 'Administrator_settings/user_confirm_delete.html', {'user': user_instance})


def user_detail(request, pk):
    """View user details."""
    # Fetch locations using raw SQL (ensure column names are correct)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, city_name FROM location")  # Ensure correct column name
        locations_list = cursor.fetchall()

    # Convert list of tuples to dictionaries
    locations = [{'id': row[0], 'name': row[1]} for row in locations_list]


    user_instance = get_object_or_404(User, pk=pk)
    form = UserForm(instance=user_instance)

    return render(request, 'Administrator_settings/user_form.html', {
        'form': form, 
        'title': 'View User', 
        'view_mode': True, 
        'locations': locations  # ✅ Pass locations here
    })

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(name=username, password=password).first()

        if user:
            request.session["username"] = user.name

            if user.is_admin:  # Check if the user is an admin
                request.session["is_admin"] = True
                request.session["location"] = None  # Admin can select location
            else:
                request.session["is_admin"] = False
                request.session["location"] = user.location  # Regular users get assigned location

            return redirect("dashboard")  # Redirect to dashboard/homepage

    return render(request, "login.html")  # Render login page


