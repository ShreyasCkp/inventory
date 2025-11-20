from django import forms
from .models import RawInwardMaterial,RawInwardMaterialSub,RmLabelGeneration
from .models import RmMaterialIssue, RmMaterialIssueSub
from master.models import ItemDetail


from django import forms
from datetime import date
from .models import RawInwardMaterial


class RawInwardMaterialForm(forms.ModelForm):
    class Meta:
        model = RawInwardMaterial
        fields =  '__all__'
 
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'grn_date': forms.DateInput(attrs={'type': 'date'}),
            'po_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Set today's date as initial for date fields
    def __init__(self, *args, **kwargs):
        super(RawInwardMaterialForm, self).__init__(*args, **kwargs)

        # Set initial value for date fields to today's date if not provided
        default_date = date.today()

        if not self.instance.pk:  # Only apply on add, not edit
            self.fields['invoice_date'].initial = default_date
            self.fields['grn_date'].initial = default_date
            self.fields['po_date'].initial = default_date


class RawInwardMaterialSubForm(forms.ModelForm):
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
        model = RawInwardMaterialSub
        fields =  '__all__'
        widgets = {
            'exp_date': forms.DateInput(attrs={'type': 'date'}),
            'mfg_date': forms.DateInput(attrs={'type': 'date'}),
            
        }

        


class RmMaterialIssueForm(forms.ModelForm):
    class Meta:
        model = RmMaterialIssue
        fields = '__all__'
        widgets = {
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }

class RmMaterialIssueSubForm(forms.ModelForm):
    class Meta:
        model = RmMaterialIssueSub
        fields = '__all__'
       


class RmLabelForm(forms.ModelForm):
    class Meta:
        model = RmLabelGeneration
        fields = '__all__'  # Include all fields
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),  # Date Picker
        }



      


