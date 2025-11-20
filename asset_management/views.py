from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from master.models import ItemDetail, VendorDetail,StoreDetail,Bag_BoxesDetails
from .forms import AmInwardMaterialForm,AmInwardMaterialItemForm,assetMaterialIssueForm,assetMaterialIssueSubForm
from .models import AmInwardMaterial, AmInwardMaterialItem,assetMaterialIssue,assetMaterialIssueSub
from datetime import date




# List of Inward Materials
def am_inward_material_list(request):
    am_inward_materials = AmInwardMaterial.objects.all()
    return render(request, 'asset_management/am_inward_material_list.html', {
        'am_inward_materials': am_inward_materials
    })

from datetime import date

def am_inward_material_add(request, pk=None): 
   # Handle both Add and Edit
    today_date = date.today().strftime("%Y-%m-%d")  # Get today's date
    item_master = ItemDetail.objects.all()
    vendors = VendorDetail.objects.all()
    stores = StoreDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    am_inward_material = None
    if pk:  # If `pk` is provided, it's an edit operation
        am_inward_material = AmInwardMaterial.objects.get(pk=pk)

    if request.method == 'POST':
        form = AmInwardMaterialForm(request.POST, instance=am_inward_material)

        if form.is_valid():
            am_inward_material = form.save(commit=False)

            # ✅ Ensure GRN Number is generated only for new records
            if not am_inward_material.grn_no:
                am_inward_material.grn_no = AmInwardMaterial.generate_next_grn_no()
            
            # ✅ Ensure GRN Date is set only if not provided
           
            am_inward_material.grn_date = date.today()
              
            
            am_inward_material.save()

            # ✅ Save Child Items (Only for Add/Edit, not View)
            if not pk:  # This ensures child items are added only in the 'Add' case
                item_codes = request.POST.getlist('item_code[]')
                item_names = request.POST.getlist('item_name[]')
                uoms = request.POST.getlist('uom[]')
                quantities = request.POST.getlist('quantity[]')

                for i in range(len(item_codes)):
                    if item_codes[i]:
                       AmInwardMaterialItem.objects.create(
                            am_inward_material=am_inward_material,
                            item_code=item_codes[i],
                            item_name=item_names[i],
                            uom=uoms[i],
                            quantity=quantities[i],
                        )

            messages.success(request, "Am Inward Material saved successfully!")
            return redirect('am_inward_material_list')

        else:
            messages.error(request, "Failed to save Inward Material.")
    else:
        # ✅ Pre-fill form data correctly
        if am_inward_material:  # Edit Mode
            form = AmInwardMaterialForm(instance=am_inward_material)
        else:  # Add Mode
            form = AmInwardMaterialForm(initial={
                "grn_no": AmInwardMaterial.generate_next_grn_no(),
                "grn_date": today_date,
            })

    return render(request, 'asset_management/am_inward_material_form.html', {
        'form': form,
        'item_master': item_master,
        'vendors': vendors,
        'stores': stores,
        'bag_types': bag_types,
        'title': 'Edit Am Inward Material' if pk else 'Add AmInward Material',
        'today_date':today_date,
        "hide_logout": True,
    })





# Edit Inward Material
# Edit Inward Material
def am_inward_material_edit(request, id):
    Aminward_material = get_object_or_404(AmInwardMaterial, pk=id)  # Correct variable name
    item_master = ItemDetail.objects.all()
    vendors = VendorDetail.objects.all()
    stores = StoreDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    if Aminward_material.grn_date:  # Use the correct variable name
        today_date = Aminward_material.grn_date.strftime('%Y-%m-%d')
    else:
        today_date = date.today().strftime('%Y-%m-%d')

    form = AmInwardMaterialForm(request.POST or None, instance=Aminward_material)  # Correct instance name
    child_items = AmInwardMaterialItem.objects.filter(am_inward_material=Aminward_material)

    subforms = [AmInwardMaterialItemForm(instance=child_item) for child_item in child_items]

    if request.method == "POST":
        if form.is_valid():
            Aminward_material = form.save(commit=False)  # Correct variable name
            Aminward_material.grn_date = form.cleaned_data.get("grn_date", date.today())  # Ensure date is saved
            Aminward_material.save()

            # Clear Old Items
            child_items.delete()

            # Retrieve Updated Items
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')

            for i in range(len(item_names)):
                AmInwardMaterialItem.objects.create(
                    am_inward_material=Aminward_material,  # Correct variable name
                    item_code=item_codes[i],
                    item_name=item_names[i],
                    uom=uoms[i],
                    quantity=quantities[i],
                )

            messages.success(request, "Inward Material updated successfully!")
            return redirect('am_inward_material_list')
        else:
            messages.error(request, "Failed to update Inward Material.")
    else:
        form = AmInwardMaterialForm(instance=Aminward_material, initial={"grn_date": today_date})  # Correct variable name

    return render(request, 'asset_management/am_inward_material_form.html', {
        'form': form,
        'title': 'Edit AmInward Material',
        'child_items': child_items,
        'item_master': item_master,
        'stores': stores,
        'subforms': subforms,
        'vendors': vendors,
        'bag_types': bag_types,
        'today_date': today_date,
        "hide_logout": True,
    })





# View Inward Material
def am_inward_material_view(request, id):
    material = get_object_or_404(AmInwardMaterial, id=id)
    vendors = VendorDetail.objects.all()
    stores = StoreDetail.objects.all()
    item_master = ItemDetail.objects.all()
    if material.grn_date:
        today_date = material.grn_date.strftime('%Y-%m-%d')
    else:
        today_date = date.today().strftime('%Y-%m-%d')
    bag_types = Bag_BoxesDetails.objects.all()
    form = AmInwardMaterialForm(instance=material, initial={"grn_date": today_date})
    child_items = AmInwardMaterialItem.objects.filter(am_inward_material=material)

  

    return render(request, 'asset_management/am_inward_material_form.html', {
        'form': form,
        'title': 'View AmInward Material',
        'child_items': child_items,
        'view_mode': True,
        'item_master': item_master,
        'stores': stores,
        'vendors': vendors,
        'bag_types': bag_types,
        'today_date': today_date,  # Ensure GRN Date is properly formatted
        "hide_logout": True,
    })



# Delete Inward Material
def am_inward_material_delete(request, id):
    material = get_object_or_404(AmInwardMaterial, id=id)
    material.delete()
    messages.success(request, "Am Inward Material deleted successfully!")
    return redirect('am_inward_material_list')


# List of RM Material Issues
def asset_material_issue_list(request):
    issues = assetMaterialIssue.objects.all()
    return render(request, 'asset_management/asset_material_issue_list.html', {'issues': issues})


def asset_material_issue_add(request):
    today_date = date.today().strftime("%Y-%m-%d")  # Get today's date
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    if request.method == 'POST':
        form = assetMaterialIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)  
            
            if not issue.iss_no:
                issue.iss_no = assetMaterialIssue.generate_next_issue_no()  # Auto-generate simple issue number

            issue.date_of_issue = date.today()  
            issue.save()  

            # Saving child records
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            stock_quantities = request.POST.getlist('stock_quantity[]')
            batch_nos = request.POST.getlist('batch_no[]')

            for i in range(len(item_codes)):
                if item_codes[i]:
                    assetMaterialIssueSub.objects.create(
                        issue=issue,
                        item_code=item_codes[i],
                        item_name=item_names[i],
                        uom=uoms[i],
                        quantity=quantities[i],
                        stock_quantity=stock_quantities[i],
                        batch_no=batch_nos[i],
                    )

            messages.success(request, "Asset Material Issue added successfully!")
            return redirect('asset_material_issue_list')
        else:
            messages.error(request, "Failed to add Asset Material Issue. Please correct the errors.")
    else:
        form = assetMaterialIssueForm(initial={
            "iss_no": assetMaterialIssue.generate_next_issue_no(),  
            "date_of_issue": today_date,  
        })

    return render(request, 'asset_management/asset_material_issue_form.html', {
        'form': form,
        'title': 'Add Asset Material Issue',
        'item_master': item_master,
        'bag_types': bag_types,
        'today_date': today_date,
        "hide_logout": True,
    })



# Edit RM Material Issue
def asset_material_issue_edit(request, id):
    issue = get_object_or_404(assetMaterialIssue, pk=id)

    # Ensure we get the existing date_of_issue or use today's date
    if issue.date_of_issue:
        today_date = issue.date_of_issue.strftime('%Y-%m-%d')
    else:
        today_date = date.today().strftime('%Y-%m-%d')

    form = assetMaterialIssueForm(request.POST or None, instance=issue)
    child_items = assetMaterialIssueSub.objects.filter(issue=issue)
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    if request.method == "POST":
        if form.is_valid():
            issue = form.save(commit=False)
            issue.date_of_issue = form.cleaned_data.get("date_of_issue", date.today())  # Ensure the date is saved
            issue.save()

            # Clear Old Items
            child_items.delete()

            # Retrieve Updated Items
            item_codes = request.POST.getlist('item_code[]')
            item_names = request.POST.getlist('item_name[]')
            uoms = request.POST.getlist('uom[]')
            quantities = request.POST.getlist('quantity[]')
            stock_quantities = request.POST.getlist('stock_quantity[]')
            batch_nos = request.POST.getlist('batch_no[]')

            for i in range(len(item_names)):
                assetMaterialIssueSub.objects.create(
                    issue=issue,
                    item_code=item_codes[i],
                    item_name=item_names[i],
                    uom=uoms[i],
                    quantity=quantities[i],
                    stock_quantity=stock_quantities[i],
                    batch_no=batch_nos[i],
                )

            messages.success(request, "Asset Material Issue updated successfully!")
            return redirect('asset_material_issue_list')
        else:
            messages.error(request, "Failed to update Asset Material Issue.")
    else:
        form = assetMaterialIssueForm(instance=issue, initial={"date_of_issue": today_date})  # Ensure date is pre-filled

    return render(request, 'asset_management/asset_material_issue_form.html', {
        'form': form,
        'title': 'Edit Asset Material Issue',
        'child_items': child_items,
        'item_master': item_master,
        'bag_types': bag_types,
        'today_date': today_date,  # Ensure today_date is passed to the template
        "hide_logout": True,
    })


 
# View RM Material Issue
def asset_material_issue_view(request, id):
    issue = get_object_or_404(assetMaterialIssue, pk=id)

    # Ensure we get the existing date_of_issue or use today's date
    if issue.date_of_issue:
        today_date = issue.date_of_issue.strftime('%Y-%m-%d')
    else:
        today_date = date.today().strftime('%Y-%m-%d')

    form = assetMaterialIssueForm(instance=issue, initial={"date_of_issue": today_date})
    child_items = assetMaterialIssueSub.objects.filter(issue=issue)
    item_master = ItemDetail.objects.all()
    bag_types = Bag_BoxesDetails.objects.all()

    return render(request, 'asset_management/asset_material_issue_form.html', {
        'form': form,
        'title': 'View Asset Material Issue',
        'child_items': child_items,
        'view_mode': True,  # If this is a read-only view
        'item_master': item_master,
        'bag_types': bag_types,
        'today_date': today_date,  # Ensure this is passed
        "hide_logout": True,
    })

 
# Delete RM Material Issue
def asset_material_issue_delete(request, id):
    issue = get_object_or_404(assetMaterialIssue, id=id)
    issue.delete()
    messages.success(request, "Asset Material Issue deleted successfully!")
    return redirect('asset_material_issue_list')



