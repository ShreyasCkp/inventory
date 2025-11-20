from django.db import models
from datetime import date

class AmInwardMaterial(models.Model):
    invoice_no = models.CharField(max_length=50)
    invoice_date = models.DateField()
    vendor_code = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=255)
    grn_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    grn_date =  models.DateField(default=date.today) 
    store = models.CharField(max_length=100)
    po_date = models.DateField()
    po_no = models.CharField(max_length=50)
    bag_type = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.grn_no:  
            self.grn_no = self.generate_next_grn_no()
        if not self.grn_date:
            self.grn_date = date.today()  # Set issue date to today
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




class AmInwardMaterialItem(models.Model):  # Moved outside of InwardMaterial
    am_inward_material = models.ForeignKey(AmInwardMaterial, on_delete=models.CASCADE, null=True, blank=True)
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_code} - {self.item_name}"


class assetMaterialIssue(models.Model):
    iss_no = models.PositiveIntegerField(unique=True, blank=True, null=True)  # Auto-incrementing issue number
    date_of_issue = models.DateField(default=date.today)  # Default to today
    issued_to_whom = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    bag_type= models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.iss_no:  
            self.iss_no = self.generate_next_issue_no()  # Generate simple issue number (1, 2, 3, ...)
        if not self.date_of_issue:
            self.date_of_issue = date.today()  # Set issue date to today (Fixed Typo ✅)
        super().save(*args, **kwargs)

    @classmethod
    def generate_next_issue_no(cls):
        last_entry = cls.objects.order_by("-iss_no").first()  # Get last issue number

        if last_entry and last_entry.iss_no:
            next_number = last_entry.iss_no + 1  # Increment last issue number
        else:
            next_number = 1  # Start from 1 if no records exist
             
        return next_number

    def __str__(self):
        return f"Issue No: {self.iss_no} - Date: {self.date_of_issue}"
 
 
class assetMaterialIssueSub(models.Model):
    issue = models.ForeignKey(assetMaterialIssue, on_delete=models.CASCADE, null=True, blank=True) 
    item_code = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    uom = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2)
 
    batch_no = models.CharField(max_length=100)
    
 
    def __str__(self):
        return f"{self.item_name} - {self.quantity}"