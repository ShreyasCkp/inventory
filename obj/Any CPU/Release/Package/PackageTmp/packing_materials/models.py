from django.db import models
from datetime import date
from master.models import ItemDetail, VendorDetail
from datetime import date

class PMLabelGenerationItem(models.Model):
    item_name = models.CharField(max_length=255)  # Item Name
    item_code = models.CharField(max_length=50)  # Item Code
    noofpacks = models.IntegerField()
    next_pack_no = models.IntegerField()
    lot_batch_no = models.CharField(max_length=255)
    packing_qty = models.IntegerField()
    receipt_date = models.DateField()

    def __str__(self):
        return f"{self.item_name} - {self.item_code}"

# Create your models here.
# models.py
from django.db import models
from datetime import date
# Create your models here.
class PackingInwardMaterial(models.Model):
    invoice_no = models.CharField(max_length=50)
    invoice_date = models.DateField()
    vendor_code = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=255)
    grn_no = models.CharField(max_length=50)
    grn_date = models.DateField(default=date.today)  # ✅ Correct default

    recieved_date = models.DateField()
    store = models.CharField(max_length=100)
    po_date = models.DateField()
    po_no = models.CharField(max_length=50)
    bag_type= models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.grn_no:
            self.grn_no = self.generate_next_grn_no()
        if not self.grn_date:
            self.grn_date = date.today()  # ✅ Ensure correct default
        super().save(*args, **kwargs)

    @classmethod
    def generate_next_grn_no(cls):
        today = date.today()
        year = today.year
        month = today.month

        # Determine Financial Year (April - March)
        if month >= 4:  # April or later (New Financial Year starts)
            start_year = year % 100
            end_year = (year + 1) % 100
        else:  # January to March (Still in previous Financial Year)
            start_year = (year - 1) % 100
            end_year = year % 100

        financial_year = f"{start_year:02d}-{end_year:02d}"

        # Get the last GRN number for the same financial year
        last_entry = cls.objects.filter(grn_no__startswith=financial_year).order_by("-id").first()

        if last_entry and last_entry.grn_no:
            last_number = int(last_entry.grn_no.split("/")[-1])
            next_number = last_number + 1
        else:
            next_number = 1

        return f"{financial_year}/{next_number:02d}"  # Example: 24-25/01, 24-25/02

    def __str__(self):
        return f"{self.id} - {self.grn_no}"



# models.py
class PackingInwardMaterialSub(models.Model):
    packing_material = models.ForeignKey('PackingInwardMaterial', on_delete=models.CASCADE, null=True, blank=True)  # Make it nullable
    
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)

  
    uom = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_bags = models.IntegerField()
    recieved_date = models.DateField()
   

    def __str__(self):
        return f"{self.item_name} -  {self.quantity} units"



class pmmaterialissue(models.Model):
    matIssueId = models.AutoField(primary_key=True)
    issue_no = models.PositiveIntegerField(unique=True, blank=True, null=True)  # Auto-incrementing issue number
    issue_date = models.DateField(default=date.today)  # Default to today 
    issue_to_whom = models.CharField(max_length=100)
    bag_types = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.issue_no:  
            self.issue_no = self.generate_next_issue_no()  # Generate simple issue number (1, 2, 3, ...)
        if not self.issue_date:
            self.issue_date = date.today()  # Set issue date to today (Fixed Typo ✅)
        super().save(*args, **kwargs)

    @classmethod
    def generate_next_issue_no(cls):
        last_entry = cls.objects.order_by("-iss_no").first()  # Get last issue number

        if last_entry and last_entry.issue_no:
            next_number = last_entry.issue_no + 1  # Increment last issue number
        else:
            next_number = 1  # Start from 1 if no records exist
             
        return next_number

    def __str__(self):
        return f"Issue No: {self.issue_no} - Date: {self.issue_date}"




class pmmaterialissuesub(models.Model):
    matIssueSubId = models.AutoField(primary_key=True)  # Explicitly set as primary key
    matIssueId = models.ForeignKey("pmmaterialissue",  on_delete=models.CASCADE,blank=True)  # Make it nullable   #on_delete=models.CASCADE, related_name="sub_issues")

    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100) 
    
    uom = models.CharField(max_length=50)
    quantity = models.IntegerField()
    stock_qty = models.IntegerField()
    total_bags = models.IntegerField()
    batch_no = models.CharField(max_length=50)  
    bags_issued = models.IntegerField()
    def __str__(self):
        return f"{self.item_name} - {self.quantity} units"



class PurchaseOrder(models.Model):
    sl_no = models.AutoField(primary_key=True)
    pono = models.CharField(max_length=255)
    po_date = models.DateField()
    vendor = models.ForeignKey(VendorDetail, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)
    upload_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='items', on_delete=models.CASCADE)
    sl_no = models.AutoField(primary_key=True)
    item_code = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    qty = models.IntegerField()

from django.contrib.auth.models import User
class UploadedFile(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    file_type = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateField() 
