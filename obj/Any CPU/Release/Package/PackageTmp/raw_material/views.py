from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from master.models import ItemDetail, VendorDetail,StoreDetail,Bag_BoxesDetails
from .forms import RawInwardMaterialForm, RawInwardMaterialSubForm,RmLabelForm
from .models import RawInwardMaterial, RawInwardMaterialSub,RmLabelGeneration
from .models import RmMaterialIssue, RmMaterialIssueSub
from .forms import RmMaterialIssueForm, RmMaterialIssueSubForm
from django.utils.timezone import now
from datetime import date
import qrcode
import base64
from io import BytesIO
from datetime import date

# List of Inward Materials
def inward_material_list(request):
    inward_materials = RawInwardMaterial.objects.all()
    return render(request, 'raw_material/inward_material_list.html', {
        'inward_materials': inward_materials
    })


from datetime import date

def inward_material_add(request):
    item_master = ItemDetail.objects.all()
    vendors = VendorDetail.objects.all()
    stores = StoreDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    # ✅ Set today's date to pass in template
    today_date = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = RawInwardMaterialForm(request.POST)

        if form.is_valid():
            inward_material = form.save(commit=False)

            # ✅ Generate GRN Number only if it's a new record
            if not inward_material.grn_no:
                inward_material.grn_no = RawInwardMaterial.generate_next_grn_no()

            inward_material.save()

            # Retrieve updated items from POST request
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            no_of_bags_list = request.POST.getlist('no_of_bags[]')
            mfg_dates = request.POST.getlist('mfg_date[]')
            exp_dates = request.POST.getlist('exp_date[]')
            lot_nos = request.POST.getlist('lot_no[]')
            repacking_batch_nos = request.POST.getlist('repacking_batch_no[]')

            for i in range(len(item_names)):
                if item_codes[i]:  # Avoid empty entries
                    RawInwardMaterialSub.objects.create(
                        inward_material=inward_material,
                        item_code=item_codes[i],
                        item_name=item_names[i],
                        uom=uoms[i],
                        quantity=quantities[i],
                        no_of_bags=no_of_bags_list[i],
                        mfg_date=mfg_dates[i] if mfg_dates[i] else date.today(),
                        exp_date=exp_dates[i] if exp_dates[i] else date.today(),
                        lot_no=lot_nos[i],
                        repacking_batch_no=repacking_batch_nos[i],
                    )
            messages.success(request, "Inward Material added successfully!")
            return redirect('inward_material_list')
        else:
            messages.error(request, "Failed to add Inward Material. Please correct the errors.")
    else:
        # ✅ Initial form with today's date pre-filled
        form = RawInwardMaterialForm(initial={
            "grn_no": RawInwardMaterial.generate_next_grn_no(),
            "grn_date": today_date,  # Default today's date for grn_date
        })

    return render(request, 'raw_material/inward_material_form.html', {
        'form': form,
        'item_master': item_master,
        'vendors': vendors,
        'stores': stores,
        'bag_types': bag_types,
        'title': 'Add Inward Material',
        'today_date': today_date,  # ✅ Pass today's date for use in template
    })


# Edit Inward Material
def inward_material_edit(request, id):
    inward_material = get_object_or_404(RawInwardMaterial, pk=id)
    item_master = ItemDetail.objects.all()
    vendors = VendorDetail.objects.all()
    stores = StoreDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    # Ensure grn_date is properly formatted and available in the form
    today_date = inward_material.grn_date.strftime('%Y-%m-%d') if inward_material.grn_date else date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = RawInwardMaterialForm(request.POST, instance=inward_material)
    else:
        form = RawInwardMaterialForm(instance=inward_material, initial={'grn_date': today_date})

    child_items = RawInwardMaterialSub.objects.filter(inward_material=inward_material)
    subforms = [RawInwardMaterialSubForm(instance=child_item) for child_item in child_items]

    if request.method == 'POST':
        if form.is_valid():
            inward_material = form.save(commit=False)
            inward_material.grn_date = form.cleaned_data.get("grn_date", date.today())  # Ensure date is saved
            inward_material.save()

            # Clear old child items
            child_items.delete()

            # Retrieve updated items from POST request
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            no_of_bags_list = request.POST.getlist('no_of_bags[]')
            mfg_dates = request.POST.getlist('mfg_date[]')
            exp_dates = request.POST.getlist('exp_date[]')
            lot_nos = request.POST.getlist('lot_no[]')
            repacking_batch_nos = request.POST.getlist('repacking_batch_no[]')

            for i in range(len(item_names)):
                RawInwardMaterialSub.objects.create(
                    inward_material=inward_material,
                    item_code=item_codes[i],
                    item_name=item_names[i],
                    uom=uoms[i],
                    quantity=quantities[i],
                    no_of_bags=no_of_bags_list[i],
                    mfg_date=mfg_dates[i],
                    exp_date=exp_dates[i],
                    lot_no=lot_nos[i],
                    repacking_batch_no=repacking_batch_nos[i],
                )

            messages.success(request, "Inward Material updated successfully!")
            return redirect('inward_material_list')
        else:
            messages.error(request, "Failed to update Inward Material.")

    return render(request, 'raw_material/inward_material_form.html', {
        'form': form,
        'title': 'Edit Inward Material',
        'child_items': child_items,
        'subforms': subforms,
        'item_master': item_master,
        'vendors': vendors,
        'stores': stores,
        'bag_types': bag_types,
        'today_date': today_date,
    })




# View Inward Material
from datetime import datetime, date

def inward_material_view(request, id):
    material = get_object_or_404(RawInwardMaterial, id=id)
    vendors = VendorDetail.objects.all()
    stores = StoreDetail.objects.all()
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()
    
    # Ensure GRN date is properly formatted as YYYY-MM-DD
    today_date = material.grn_date.strftime('%Y-%m-%d') if material.grn_date else date.today().strftime('%Y-%m-%d')
    
    # Initial value for grn_date in the form
    form = RawInwardMaterialForm(instance=material, initial={"grn_date": today_date})

    child_items = RawInwardMaterialSub.objects.filter(inward_material=material)

    # ✅ Pass 'now' and 'today_date' explicitly to the template
    return render(request, 'raw_material/inward_material_form.html', {
        'form': form,
        'title': 'View Inward Material',
        'child_items': child_items,
        'view_mode': True,
        'item_master': item_master,
        'stores': stores,
        'vendors': vendors,
        'bag_types': bag_types,
        'today_date': today_date,
        'now': datetime.now(),
    })



# Delete Inward Material
def inward_material_delete(request, id):
    material = get_object_or_404(RawInwardMaterial, id=id)
    material.delete()
    messages.success(request, "Inward Material deleted successfully!")
    return redirect('inward_material_list')




# List of RM Material Issues
def rm_material_issue_list(request):
    issues = RmMaterialIssue.objects.all()
    return render(request, 'raw_material/rm_material_issue_list.html', {'issues': issues})

# Add New RM Material Issue
def rm_material_issue_add(request):
    today_date = date.today()  # Get today's date as date object
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    if request.method == 'POST':
        form = RmMaterialIssueForm(request.POST)

        if form.is_valid():
            issue = form.save(commit=False)

            # Auto-generate issue number if applicable
            if not issue.iss_no:
                issue.iss_no = RmMaterialIssue.generate_next_issue_no()

            # Save date_of_issue correctly (use user-provided date or fallback to today)
            issue.date_of_issue = form.cleaned_data.get("date_of_issue", date.today())
            issue.save()

            # Saving child records
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            stock_quantities = request.POST.getlist('stock_quantity[]')
            total_bags = request.POST.getlist('total_bags[]')
            batch_nos = request.POST.getlist('batch_no[]')
            bags_issued = request.POST.getlist('bags_issued[]')

            for i in range(len(item_codes)):
                if item_codes[i]:
                    RmMaterialIssueSub.objects.create(
                        issue=issue,
                        item_code=item_codes[i],
                        item_name=item_names[i],
                        uom=uoms[i],
                        quantity=quantities[i],
                        stock_quantity=stock_quantities[i],
                        total_bags=total_bags[i],
                        batch_no=batch_nos[i],
                        bags_issued=bags_issued[i],
                    )

            messages.success(request, "RM Material Issue added successfully!")
            return redirect('rm_material_issue_list')
        else:
            messages.error(request, "Failed to add RM Material Issue. Please correct the errors.")
    else:
        # Correct initial data setup for the form
        form = RmMaterialIssueForm(initial={
            "iss_no": RmMaterialIssue.generate_next_issue_no(),
            "date_of_issue": today_date,
        })

    return render(request, 'raw_material/rm_material_issue_form.html', {
        'form': form,
        'title': 'Add RM Material Issue',
        'item_master': item_master,
        'bag_types': bag_types,
    })




# Edit RM Material Issue
def rm_material_issue_edit(request, id):
    issue = get_object_or_404(RmMaterialIssue, pk=id)

    # Correctly bind instance without initial
    form = RmMaterialIssueForm(request.POST or None, instance=issue)
    child_items = RmMaterialIssueSub.objects.filter(issue=issue)
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    if request.method == "POST":
        if form.is_valid():
            issue = form.save(commit=False)
            issue.date_of_issue = form.cleaned_data.get("date_of_issue", date.today())  # Save valid date
            issue.save()

            # Clear Old Items
            child_items.delete()

            # Retrieve Updated Items
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            stock_quantities = request.POST.getlist('stock_quantity[]')
            total_bags = request.POST.getlist('total_bags[]')
            batch_nos = request.POST.getlist('batch_no[]')
            bags_issued = request.POST.getlist('bags_issued[]')

            for i in range(len(item_codes)):
                if item_codes[i]:  # Avoid creating empty records
                    RmMaterialIssueSub.objects.create(
                        issue=issue,
                        item_code=item_codes[i],
                        item_name=item_names[i],
                        uom=uoms[i],
                        quantity=quantities[i],
                        stock_quantity=stock_quantities[i],
                        total_bags=total_bags[i],
                        batch_no=batch_nos[i],
                        bags_issued=bags_issued[i],
                    )

            messages.success(request, "RM Material Issue updated successfully!")
            return redirect('rm_material_issue_list')
        else:
            messages.error(request, "Failed to update RM Material Issue. Please check for errors.")

    return render(request, 'raw_material/rm_material_issue_form.html', {
        'form': form,
        'title': 'Edit RM Material Issue',
        'child_items': child_items,
        'item_master': item_master,
        'bag_types': bag_types,
        'today_date': issue.date_of_issue.strftime('%Y-%m-%d') if issue.date_of_issue else date.today().strftime('%Y-%m-%d'),
    })


# View RM Material Issue
def rm_material_issue_view(request, id):
    issue = get_object_or_404(RmMaterialIssue, pk=id)

    form = RmMaterialIssueForm(instance=issue)  # Correct instance binding
    child_items = RmMaterialIssueSub.objects.filter(issue=issue)
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    return render(request, 'raw_material/rm_material_issue_form.html', {
        'form': form,
        'title': 'View RM Material Issue',
        'child_items': child_items,
        'view_mode': True,  # Indicates this is a read-only view
        'item_master': item_master,
        'bag_types': bag_types,
        'date_of_issue': issue.date_of_issue.strftime('%Y-%m-%d') if issue.date_of_issue else '',
    })


# Delete RM Material Issue
def rm_material_issue_delete(request, id):
    issue = get_object_or_404(RmMaterialIssue, id=id)
    issue.delete()
    messages.success(request, "RM Material Issue deleted successfully!")
    return redirect('rm_material_issue_list')


def create_rm_label(request):
    vendors = VendorDetail.objects.all()
    item_master = ItemDetail.objects.all()

    if request.method == "POST":
        form = RmLabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rm_label_list')
    else:
        form = RmLabelForm()

    return render(request, 'raw_material/create_rm_label.html', {
        'form': form,
        'vendors': vendors,   # ✅ Passing vendor data
        'item_master': item_master,  # ✅ Passing item data
    })


def rm_label_list(request):
    labels = RmLabelGeneration.objects.all()
    return render(request, 'raw_material/rm_label_list.html', {'labels': labels})

def edit_rm_label(request, pk):
    label = get_object_or_404(RmLabelGeneration, pk=pk)
    vendors = VendorDetail.objects.all()
    item_master = ItemDetail.objects.all()

    if request.method == "POST":
        form = RmLabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect('rm_label_list')
    else:
        form = RmLabelForm(instance=label)

    return render(request, 'raw_material/edit_rm_label.html', {
        'form': form,
        'label': label,
        'vendors': vendors,  # ✅ Passing vendor data
        'item_master': item_master,  # ✅ Passing item data
    })


def delete_rm_label(request, pk):
    label = get_object_or_404(RmLabelGeneration, pk=pk)
    if request.method == "POST":
        label.delete()
        return redirect('rm_label_list')
    return render(request, 'raw_material/delete_rm_label.html', {'label': label})

def print_rm_label(request, pk):
    label = get_object_or_404(RmLabelGeneration, pk=pk)

    # Generate QR Code
    qr_data = f"Vendor: {label.vendor_name}\nItem: {label.item_name}\nBatch: {label.batch_no}"
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode()

    return render(request, 'raw_material/print_rm_label.html', {'label': label, 'qr_code_base64': qr_base64})


from .forms import RmLabelForm  # Make sure to import the correct form
def rm_label_view(request, pk):
    label = get_object_or_404(RmLabelGeneration, pk=pk)
    vendors = VendorDetail.objects.all()
    item_master = ItemDetail.objects.all()

    form = RmLabelForm(instance=label)  # Bind the form to the model instance
    
    # Pass view_mode as True to disable form fields in view mode
    return render(request, 'raw_material/create_rm_label.html', {
        'form': form,
        'vendors': vendors,
        'item_master': item_master,
        'view_mode': True,  # Set to True for view mode (readonly)
    })

