from django.db import models
from master.models import CustomerDetail, ItemDetail  # Import from master app
from django.db import models
from datetime import date

# Create your models here.
from django.db import models
from datetime import date

class FGInwardMaterial(models.Model):
    inward_no = models.CharField(max_length=50)
    inward_date = models.DateField()
    store = models.CharField(max_length=100)
    po_date = models.DateField()
    po_no = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.inward_no


class FGInwardMaterialSub(models.Model):
    inward_material = models.ForeignKey(FGInwardMaterial, on_delete=models.CASCADE, null=True, blank=True)  
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    box_no = models.IntegerField()
    mfg_date = models.DateField()
    batch_no = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.item_name} - {self.quantity} units"


class FGLabelGeneration(models.Model):
    item_code = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)  
    item_name = models.CharField(max_length=255, editable=False)  
    batch_no = models.CharField(max_length=255)
    packing_qty = models.IntegerField()
    no_of_bags = models.IntegerField()
    next_bag_no = models.CharField(max_length=255)
    date_of_packing = models.DateField()
    date_of_expiry = models.DateField()

    def __str__(self):
        return f'{self.item_code} - {self.item_name}'


class PackingSlip(models.Model):
    ps_no = models.CharField(max_length=50)
    ps_date = models.DateField()
    customer = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE, related_name='fg_packing_slips')  
    po_no = models.CharField(max_length=50)
    po_date = models.DateField()
    mode_of_transport = models.CharField(max_length=50)
    transport_form = models.CharField(max_length=50)
    transfer_to_vehicle_no = models.CharField(max_length=50)
    transport_name = models.CharField(max_length=50)
    trans_to = models.CharField(max_length=50)


    def __str__(self):
        return f'Packing Slip {self.ps_no} for {self.customer.customer_name}'


class PackingSlipItem(models.Model):
    packing_slip = models.ForeignKey(PackingSlip, related_name='items', on_delete=models.CASCADE)  # Make it nullable
    item_code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    item_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=50)
    box_bags = models.IntegerField()
    batch_no = models.CharField(max_length=50)
    qty = models.IntegerField()
    bal_qty = models.IntegerField()
    stock_qty = models.IntegerField()

    def __str__(self):
        return f'{self.item_code} - {self.item_name}'


