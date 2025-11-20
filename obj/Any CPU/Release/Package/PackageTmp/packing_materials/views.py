from datetime import date, datetime
from io import BytesIO

import base64
import qrcode

from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    FileUploadForm,
    PackingInwardMaterialForm,
    PackingInwardMaterialSubForm,
    PMLabelGenerationForm,
    pmmaterialissueForm,
    pmmaterialissuesubForm,
    PurchaseOrderForm,
    PurchaseOrderItemForm,
)
from .models import (
    PMLabelGenerationItem,
    PackingInwardMaterial,
    PackingInwardMaterialSub,
    pmmaterialissue,
    pmmaterialissuesub,
    PurchaseOrder,
    PurchaseOrderItem,
    UploadedFile,
)

from master.models import ItemDetail, VendorDetail, StoreDetail, Bag_BoxesDetails


def create_pm_label(request):
    item_master = ItemDetail.objects.all()

    if request.method == "POST":
        # Get data from POST
        noofpacks_list = request.POST.getlist("noofpacks")
        next_pack_no_list = request.POST.getlist("next_pack_no")
        lot_batch_no_list = request.POST.getlist("lot_batch_no")
        packing_qty_list = request.POST.getlist("packing_qty")
        item_code_list = request.POST.getlist("item_code")
        item_name_list = request.POST.getlist("item_name")
        receipt_date = request.POST.get("receipt_date")  # Get the date as string

        # Convert receipt_date string to a date object
        try:
            receipt_date = datetime.strptime(receipt_date, '%Y-%m-%d').date()
        except ValueError:
            # Handle the case where the date format is incorrect
            messages.error(request, "Invalid receipt date format. Please try again.")
            return redirect("create_pm_label")

        # Iterate and save data
        for i in range(len(item_code_list)):
            if item_code_list[i] and item_name_list[i]:
                PMLabelGenerationItem.objects.create(
                    item_code=item_code_list[i],
                    item_name=item_name_list[i],
                    noofpacks=noofpacks_list[i],
                    next_pack_no=next_pack_no_list[i],
                    lot_batch_no=lot_batch_no_list[i],
                    packing_qty=packing_qty_list[i],
                    receipt_date=receipt_date,  # Save the converted date
                )
        messages.success(request, "PM Label created successfully!")
        return redirect("pm_label_list")

    # If GET request
    else:
        form = PMLabelGenerationForm()

    return render(
        request, "packing_materials/create_pm_label.html",
        {
            "form": form,
            "item_master": item_master,
            "today": date.today(),
            "hide_logout": True,
        },
    )

def pm_label_list(request):
    labels = PMLabelGenerationItem.objects.all()
    return render(request, 'packing_materials/pm_label_list.html', {'labels': labels})
from django.views import View


from datetime import date

def pm_label_view(request, pk):
    label = get_object_or_404(PMLabelGenerationItem, pk=pk)
    item_master = ItemDetail.objects.all()

    form = PMLabelGenerationForm(instance=label, item_master=item_master)

    context = {
        'form': form,
        'item_master': item_master,
        'view_mode': True,  # Set to True for view mode (readonly)
        'today': date.today(),
    }

    return render(request, 'packing_materials/create_pm_label.html', context)


def edit_pm_label(request, pk):
    # Retrieve the label instance
    label = get_object_or_404(PMLabelGenerationItem, pk=pk)
    item_master = ItemDetail.objects.all()

    if request.method == "POST":
        # Bind the form with POST data and the instance
        form = PMLabelGenerationForm(request.POST, instance=label, item_master=item_master)
        if form.is_valid():
            # Save the updated instance
            form.save()
            messages.success(request, "PM Label updated successfully!")
            return redirect('pm_label_list')
        else:
            # Debugging: Print form errors to console
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        # Populate the form with instance data for GET request
        form = PMLabelGenerationForm(instance=label, item_master=item_master)

    # Render the template with context
    return render(request, 'packing_materials/create_pm_label.html', {
        'form': form,
        'label': label,
        'item_master': item_master,
        'view_mode': False,  # Ensure view_mode is False for editing
    })

def delete_pm_label(request, pk):
    label = get_object_or_404(PMLabelGenerationItem, pk=pk)
    label.delete()
    messages.success(request, "PM Label Generation deleted successfully!")
    return redirect('pm_label_list')

def print_pm_label(request, pk):
    label = get_object_or_404(PMLabelGenerationItem, pk=pk)

    # Generate QR Code
    qr_data = f"Item: {label.item_name}\nBatch: {label.lot_batch_no}\nReceipt Date: {label.receipt_date}"
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode()

    return render(request, 'packing_materials/print_pm_label.html', {'label': label, 'qr_code_base64': qr_base64})




# List of Inward Materials
def packing_material_list(request):
    packing_materials = PackingInwardMaterial.objects.all()
    return render(request, 'packing_materials/packing_material_list.html', {
        'packing_materials': packing_materials
    })


# Add New Inward Material
def packing_material_add(request):
    item_master = ItemDetail.objects.all()
    vendors=VendorDetail.objects.all()
    stores=StoreDetail.objects.all()
    bag_types=Bag_BoxesDetails.objects.all()

    if request.method == 'POST':
        form =PackingInwardMaterialForm(request.POST)

        if form.is_valid():
            # Save Parent (Inward Material)
            packing_material = form.save()

            # Save Child (Item Details)
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')

            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            no_of_bags = request.POST.getlist('no_of_bags[]')
            recieved_dates = request.POST.getlist('recieved_date[]')
            

            for i in range(len(item_codes)):
                if item_codes[i]:
                    PackingInwardMaterialSub.objects.create(
                        packing_material=packing_material,
                        item_code=item_codes[i],
                        item_name=item_names[i],
                        uom=uoms[i],
                        quantity=quantities[i],
                        no_of_bags=no_of_bags[i],
                        recieved_date=recieved_dates[i],
                        

                    )

            messages.success(request, "packing Material added successfully!")
            return redirect('packing_material_list')
        else:
            messages.error(request, "Failed to add packing Material. Please correct the errors.")
    else:
        form = PackingInwardMaterialForm()

    return render(request, 'packing_materials/packing_material_form.html', {
        'form': form,
        'item_master': item_master,
        'vendors':vendors,
        'stores':stores,
        'bag_types':bag_types,
        'title': 'Add packing Material'
    })


# Edit Inward Material
def packing_material_edit(request, id):
    packing_material = get_object_or_404(PackingInwardMaterial, pk=id)
    form = PackingInwardMaterialForm(request.POST or None, instance=packing_material)
    child_items = PackingInwardMaterialSub.objects.filter(packing_material=packing_material)
    item_master = ItemDetail.objects.all()  # Fetch all item details
    vendors=VendorDetail.objects.all()
    stores=StoreDetail.objects.all()
    bag_types=Bag_BoxesDetails.objects.all()


    # Create a form instance with existing data for each child item
    subforms = [PackingInwardMaterialSubForm(instance=child_item) for child_item in child_items]

    if request.method == "POST":
        if form.is_valid():
            form.save()

            # Clear Old Items
            child_items.delete()

            # Retrieve Updated Items
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            no_of_bags = request.POST.getlist('no_of_bags[]')
            recieved_dates = request.POST.getlist('recieved_date[]')

            for i in range(len(item_names)):
                PackingInwardMaterialSub.objects.create(
                    packing_material=packing_material,
                    item_code=item_codes[i],
                    item_name=item_names[i],
                    uom=uoms[i],
                    quantity=quantities[i],
                    no_of_bags=no_of_bags[i],
                   recieved_date=recieved_dates[i],
                        
                )

            messages.success(request, "Inward Material updated successfully!")
            return redirect('packing_material_list')
        else:
            messages.error(request, "Failed to update Inward Material.")

    return render(request, 'packing_materials/packing_material_form.html', {
        'form': form,
        'title': 'Edit packing Material',
        'child_items': child_items,  # Pass child items
        'item_master': item_master,
        'stores':stores,
        'subforms': subforms,
        'vendors':vendors,
        'bag_types':bag_types,


    })


# View Inward Material
def packing_material_view(request, id):
    material = get_object_or_404(PackingInwardMaterial, id=id)
    form = PackingInwardMaterialForm(instance=material)
    child_items = PackingInwardMaterialSub.objects.filter(packing_material=material)
    item_master = ItemDetail.objects.all()
    vendors=VendorDetail.objects.all()
    stores=StoreDetail.objects.all()
    bag_types=Bag_BoxesDetails.objects.all()



    return render(request, 'packing_materials/packing_material_form.html', {
        'form': form,
        'title': 'View packing Material',
        'child_items': child_items,
        'view_mode': True,
        'item_master': item_master,
        'stores':stores,
        'vendors':vendors,
        'bag_types':bag_types,


    })


# Delete Inward Material
def packing_material_delete(request, id):
    material = get_object_or_404(PackingInwardMaterial, id=id)
    material.delete()
    messages.success(request, "Inward Material deleted successfully!")
    return redirect('packing_material_list')

def get_items(request):
    items = list(ItemDetail.objects.values('item_code', 'item_name', 'uom'))
    return JsonResponse({'items': items})

# List of PM Material Issues
def pm_material_issue_list(request):
    matIssueIds = pmmaterialissue.objects.all()
    return render(request, 'packing_materials/pm_material_issue_list.html', {
        'matIssueIds': matIssueIds
    })


def pm_material_issue_add(request):
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    if request.method == 'POST':
        form = pmmaterialissueForm(request.POST)

        if form.is_valid():
            matIssue = form.save(commit=False)  # Don't save yet
            
            # Use user-provided issue_no or generate automatically
            if not matIssue.issue_no:
                last_issue = pmmaterialissue.objects.order_by('-matIssueId').first()
                last_number = int(last_issue.issue_no.split('-')[-1]) if last_issue and last_issue.issue_no else 0
                matIssue.issue_no = f"ISSUE-{last_number + 1:04d}"

            matIssue.save()  # Now save to DB
            
            # Save Child Items
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            stock_qtys = request.POST.getlist('stock_qty[]')
            total_bags = request.POST.getlist('total_bags[]')
            batch_nos = request.POST.getlist('batch_no[]')
            bags_issued = request.POST.getlist('bags_issued[]')

            for i in range(len(item_codes)):
                if item_codes[i]:  
                    pmmaterialissuesub.objects.create(
                        matIssueId=matIssue,
                        item_code=item_codes[i],
                        item_name=item_names[i],
                        uom=uoms[i],
                        quantity=quantities[i],
                        stock_qty=stock_qtys[i],
                        total_bags=total_bags[i],
                        batch_no=batch_nos[i],
                        bags_issued=bags_issued[i],
                    )

            messages.success(request, "PM Material Issue added successfully!")
            return redirect('pm_material_issue_list')
        else:
            messages.error(request, "Failed to add PM Material Issue. Please correct the errors.")
    else:
        form = pmmaterialissueForm()

    return render(request, 'packing_materials/pm_material_issue_form.html', {
        'form': form,
        'item_master': item_master,
        'bag_types': bag_types,
        'title': 'Add PM Material Issue'
    })




# Edit PM Material Issue
def pm_material_issue_edit(request, matIssueId):
    matIssueId = get_object_or_404(pmmaterialissue, pk=matIssueId)
    form = pmmaterialissueForm(request.POST or None, instance=matIssueId)
    child_items = pmmaterialissuesub.objects.filter(matIssueId=matIssueId)
    item_master = ItemDetail.objects.all()
    bag_types=Bag_BoxesDetails.objects.all()
    subforms = [pmmaterialissuesubForm(instance=child) for child in child_items]
    
    # Create a form instance with existing data for each child item
    subforms = [pmmaterialissuesubForm(instance=child_item) for child_item in child_items]


    if request.method == "POST":
        if form.is_valid():
            form.save()
            
            child_items.delete()
            
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            stock_qtys = request.POST.getlist('stock_qty[]')
            total_bags = request.POST.getlist('total_bags[]')
            batch_nos = request.POST.getlist('batch_no[]')
            bags_issued = request.POST.getlist('bags_issued[]')
            
            for i in range(len(item_codes)):
                pmmaterialissuesub.objects.create(
                    matIssueId=matIssueId,
                    item_code=item_codes[i],
                    item_name=item_names[i],
                    uom=uoms[i],
                    quantity=quantities[i],
                    stock_qty=stock_qtys[i],
                    total_bags=total_bags[i],
                    batch_no=batch_nos[i],
                    bags_issued=bags_issued[i],
                )
            
            messages.success(request, "PM Material Issue updated successfully!")
            return redirect('pm_material_issue_list')
        else:
            messages.error(request, "Failed to update PM Material Issue.")
    
    return render(request, 'packing_materials/pm_material_issue_form.html', {
        'form': form,
        'title': 'Edit PM Material Issue',
        'child_items': child_items,
        'item_master': item_master,
        'bag_types':bag_types,
        'subforms': subforms,
    })

# View PM Material Issue
def pm_material_issue_view(request, matIssueId):
    matIssueId = get_object_or_404(pmmaterialissue, matIssueId=matIssueId)
    form = pmmaterialissueForm(instance=matIssueId)
    child_items = pmmaterialissuesub.objects.filter(matIssueId=matIssueId)
    item_master = ItemDetail.objects.all()
    bag_types=Bag_BoxesDetails.objects.all()
    return render(request, 'packing_materials/pm_material_issue_form.html', {
        'form': form,
        'title': 'View PM Material Issue',
        'child_items': child_items,
        'view_mode': True,
        'item_master': item_master,
        'bag_types':bag_types,
    })

# Delete PM Material Issue
def pm_material_issue_delete(request, matIssueId):
    matIssueId = get_object_or_404(pmmaterialissue, matIssueId=matIssueId)
    matIssueId.delete()
    messages.success(request, "PM Material Issue deleted successfully!")
    return redirect('pm_material_issue_list')

def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'packing_materials/purchase_order_list.html', {'orders': orders})

from django.shortcuts import get_object_or_404

def purchase_order_detail(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    vendors = VendorDetail.objects.all()
    users = User.objects.all()
    child_items = UploadedFile.objects.filter(purchase_order=purchase_order)

    form = PurchaseOrderForm(instance=purchase_order)

    return render(request, 'packing_materials/purchase_order_form.html', {
        'form': form,
        'title': 'View Purchase Order',
        'vendors': vendors,
        'users': users,
        'child_items': child_items,
        'view_mode': True,  # Important for template to become read-only
    })



from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import PurchaseOrder, UploadedFile, VendorDetail
from .forms import PurchaseOrderForm
from django.contrib.auth.models import User

def purchase_order_create(request):
    today_date = date.today()
    vendors = VendorDetail.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, request.FILES)

        if form.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.po_date = form.cleaned_data.get("po_date", today_date)
            purchase_order.save()

            # --- Handle child UploadedFile entries ---
            file_names = request.POST.getlist('child_file_name[]')
            file_urls = request.POST.getlist('child_file_url[]')
            file_types = request.POST.getlist('child_file_type[]')
            uploaded_bys = request.POST.getlist('child_uploaded_by[]')
            upload_dates = request.POST.getlist('child_upload_date[]')

            for i in range(len(file_names)):
                if file_names[i]:  # Only if file name is given
                    file_url = file_urls[i] if i < len(file_urls) else ''
                    file_type = file_types[i] if i < len(file_types) else ''
                    uploaded_by_input = uploaded_bys[i].strip() if i < len(uploaded_bys) else ''
                    upload_date = upload_dates[i] if i < len(upload_dates) and upload_dates[i] else today_date

                    uploaded_by_user = None
                    if uploaded_by_input:
                        try:
                            uploaded_by_user = User.objects.get(username__iexact=uploaded_by_input)
                        except User.DoesNotExist:
                            uploaded_by_user = None
                            messages.warning(request, f"User '{uploaded_by_input}' not found. Please check username.")

                    # Final fallback
                    if uploaded_by_user is None and request.user.is_authenticated:
                        uploaded_by_user = request.user

                    # Finally create
                    UploadedFile.objects.create(
                        purchase_order=purchase_order,
                        file_name=file_names[i],
                        file_url=file_url,
                        file_type=file_type,
                        uploaded_by=uploaded_by_user,
                        upload_date=upload_date,
                    )


            messages.success(request, "Purchase Order created successfully!")
            return redirect('purchase_order_list')
        else:
            messages.error(request, "Failed to create Purchase Order. Please correct the errors.")
    else:
        form = PurchaseOrderForm(initial={
            "po_date": today_date,
        })

    return render(request, 'packing_materials/purchase_order_form.html', {
        'form': form,
        'title': 'Create Purchase Order',
        'vendors': vendors,
        'users': users,  # add this line

    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import date
from .models import PurchaseOrder, UploadedFile, VendorDetail
from .forms import PurchaseOrderForm
from django.contrib.auth.models import User

def purchase_order_edit(request, pk):
    today_date = date.today()
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    vendors = VendorDetail.objects.all()
    users = User.objects.all()
    child_items = UploadedFile.objects.filter(purchase_order=purchase_order)

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, request.FILES, instance=purchase_order)

        if form.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.po_date = form.cleaned_data.get("po_date", today_date)
            purchase_order.save()

            # Remove existing child records
            UploadedFile.objects.filter(purchase_order=purchase_order).delete()

            # Fetch new child data
            file_names = request.POST.getlist('child_file_name[]')
            file_urls = request.POST.getlist('child_file_url[]')
            file_types = request.POST.getlist('child_file_type[]')
            uploaded_bys = request.POST.getlist('child_uploaded_by[]')
            upload_dates = request.POST.getlist('child_upload_date[]')

            for i in range(len(file_names)):
                if file_names[i]:  # Only if file name is given
                    file_url = file_urls[i] if i < len(file_urls) else ''
                    file_type = file_types[i] if i < len(file_types) else ''
                    uploaded_by_input = uploaded_bys[i].strip() if i < len(uploaded_bys) else ''
                    upload_date = upload_dates[i] if i < len(upload_dates) and upload_dates[i] else today_date

                    uploaded_by_user = None
                    if uploaded_by_input:
                        try:
                            uploaded_by_user = User.objects.get(username__iexact=uploaded_by_input)
                        except User.DoesNotExist:
                            uploaded_by_user = None
                            messages.warning(request, f"User '{uploaded_by_input}' not found. Please check username.")

                    if uploaded_by_user is None and request.user.is_authenticated:
                        uploaded_by_user = request.user

                    UploadedFile.objects.create(
                        purchase_order=purchase_order,
                        file_name=file_names[i],
                        file_url=file_url,
                        file_type=file_type,
                        uploaded_by=uploaded_by_user,
                        upload_date=upload_date,
                    )

            messages.success(request, "Purchase Order updated successfully!")
            return redirect('purchase_order_list')
        else:
            messages.error(request, "Failed to update Purchase Order. Please correct the errors.")
    else:
        form = PurchaseOrderForm(instance=purchase_order)

    return render(request, 'packing_materials/purchase_order_form.html', {
        'form': form,
        'title': 'Edit Purchase Order',
        'vendors': vendors,
        'users': users,
        'child_items': child_items,
        'view_mode': False,
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def purchase_order_delete(request, pk):
    if request.method == 'POST':
        purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
        purchase_order.delete()
        messages.success(request, "Purchase Order deleted successfully!")
        return redirect('purchase_order_list')
    else:
        messages.error(request, "Invalid request.")
        return redirect('purchase_order_list')


def pm_label_generation_item_list(request, pm_label_generation_id):
    pm_label_generation = get_object_or_404(PMLabelGenerationItem, id=pm_label_generation_id)
    pm_label_generation_items = PMLabelGenerationItem.objects.filter(pm_label_generation=pm_label_generation)
    
    return render(request, 'packing_materials/pm_label_generation_item_list.html', {
        'pm_label_generation': pm_label_generation,
        'pm_label_generation_items': pm_label_generation_items,
    })



from .models import UploadedFile

def edit_file(request, pk):
    file = UploadedFile.objects.get(pk=pk)
    if request.method == "POST":
        file.file_name = request.POST.get('file_name', file.file_name)
        file.save()
        return redirect('purchase_order_detail', pk=file.purchase_order.pk)
    return render(request, 'packing_materials/edit_file.html', {'file': file})

def delete_file(request, pk):
    file = UploadedFile.objects.get(pk=pk)
    order_pk = file.purchase_order.pk
    file.delete()
    return redirect('purchase_order_detail', pk=order_pk)



def save_uploaded_files(request):
    if request.method == "POST":
        files = request.FILES.getlist("files[]")  # Get all uploaded files
        file_types = request.POST.getlist("file_types[]")  # Get corresponding file types

        if not files:
            return JsonResponse({"success": False, "error": "No files received."}, status=400)

        saved_files = []
        for file, file_type in zip(files, file_types):
            file_name = f"uploads/{file.name}"
            file_path = default_storage.save(file_name, ContentFile(file.read()))  # Save file

            saved_files.append({
                "file_type": file_type,
                "file_name": os.path.basename(file_path),
                "file_url": default_storage.url(file_path),
            })

        return JsonResponse({"success": True, "files": saved_files})
    
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


