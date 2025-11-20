from django import forms
from django.forms import modelformset_factory
from master.models import ItemDetail, CustomerDetail  
from .models import FGInwardMaterial, FGInwardMaterialSub, FGLabelGeneration, PackingSlip, PackingSlipItem


class FGInwardMaterialForm(forms.ModelForm):
    class Meta:
        model = FGInwardMaterial
        fields = '__all__'
        widgets = {
            'inward_date': forms.DateInput(attrs={'type': 'date'}),
            'po_date': forms.DateInput(attrs={'type': 'date'}),
        }


class FGInwardMaterialSubForm(forms.ModelForm):
    item_code = forms.ModelChoiceField(
        queryset=ItemDetail.objects.all(),
        empty_label="Select Item Code",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    item_name = forms.CharField(
        required=False,  
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = FGInwardMaterialSub
        fields = '__all__'
        widgets = {
            'mfg_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PackingSlipForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=CustomerDetail.objects.all(),
        empty_label="Select Customer",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PackingSlip
        fields = '__all__'
        widgets = {
            'po_date': forms.DateInput(attrs={'type': 'date'}),
            'ps_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PackingSlipItemForm(forms.ModelForm):
    class Meta:
        model = PackingSlipItem
        fields = '__all__'


PackingSlipItemFormSet = modelformset_factory(PackingSlipItem, form=PackingSlipItemForm, extra=1)


class FGLabelGenerationForm(forms.ModelForm):
    class Meta:
        model = FGLabelGeneration
        fields = '__all__'


class FileUploadForm(forms.Form):
    file = forms.FileField()