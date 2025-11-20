from django import forms
from .models import PMLabelGenerationItem,PackingInwardMaterial,PackingInwardMaterialSub, PurchaseOrder, PurchaseOrderItem,pmmaterialissue, pmmaterialissuesub
from master.models import ItemDetail

class PMLabelGenerationForm(forms.ModelForm):
    class Meta:
        model = PMLabelGenerationItem
        fields = '__all__'  # Include all fields
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Use ChoiceField for dropdowns
    item_code = forms.ChoiceField(
        choices=[],  # Choices will be populated dynamically
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    item_name = forms.ChoiceField(
        choices=[],  # Choices will be populated dynamically
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        # Add dynamic choices for the dropdowns
        item_master = kwargs.pop('item_master', [])
        super().__init__(*args, **kwargs)
        self.fields['item_code'].choices = [(item.item_code, item.item_code) for item in item_master]
        self.fields['item_name'].choices = [(item.item_name, item.item_name) for item in item_master]


# forms.py
from django import forms
from .models import PackingInwardMaterial
from datetime import date

class PackingInwardMaterialForm(forms.ModelForm):
    class Meta:
        model = PackingInwardMaterial
        fields = '__all__'
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'grn_date': forms.DateInput(attrs={'type': 'date'}),
            'po_date': forms.DateInput(attrs={'type': 'date'}),
            'recieved_date': forms.DateInput(attrs={'type': 'date'}),
        }
        # Set today's date as initial for date fields
    def __init__(self, *args, **kwargs):
        super(PackingInwardMaterialForm, self).__init__(*args, **kwargs)

        # Set initial value for date fields to today's date if not provided
        default_date = date.today()

        if not self.instance.pk:  # Only apply on add, not edit
            self.fields['invoice_date'].initial = default_date
            self.fields['grn_date'].initial = default_date
            self.fields['po_date'].initial = default_date



class PackingInwardMaterialSubForm(forms.ModelForm):
    item_code = forms.ModelChoiceField(
        queryset=ItemDetail.objects.all(),
        empty_label="Select Item Code",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    item_name = forms.ModelChoiceField(
        queryset=ItemDetail.objects.all(),
        empty_label="Select Item Name",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = PackingInwardMaterialSub
        fields =  '__all__'
        widgets = {
            'recieved_date': forms.DateInput(attrs={'type': 'date'}),
        }

class pmmaterialissueForm(forms.ModelForm):
    class Meta:
        model = pmmaterialissue
        fields = '__all__'

class pmmaterialissuesubForm(forms.ModelForm):
    class Meta:
        model = pmmaterialissuesub
        fields = '__all__'

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['pono', 'po_date', 'vendor', 'remarks', 'upload_file']

class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['item_code', 'qty']

from .models import UploadedFile  # Ensure this model exists

from django.forms import DateTimeInput
from datetime import date

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = '__all__'
        widgets = {
            'upload_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['file_url'].required = False


