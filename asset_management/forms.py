from django import forms
from .models import AmInwardMaterial, AmInwardMaterialItem,assetMaterialIssue,assetMaterialIssueSub  # Fixed import
from master.models import ItemDetail
from datetime import date

class AmInwardMaterialForm(forms.ModelForm):
    grn_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        initial=date.today  # Set initial default
    )
    class Meta:
        model = AmInwardMaterial
        fields = '__all__'
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'grn_date': forms.DateInput(attrs={'type': 'date'}),
            'po_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AmInwardMaterialItemForm(forms.ModelForm):  # Renamed to avoid conflicts
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
        model = AmInwardMaterialItem
        fields = '__all__'


class assetMaterialIssueForm(forms.ModelForm):
    class Meta:
        model = assetMaterialIssue
        fields = '__all__'
        widgets = {
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }
 
class assetMaterialIssueSubForm(forms.ModelForm):
    class Meta:
        model = assetMaterialIssueSub
        fields = '__all__'