from django.db import models
from django.db.models import Sum
from raw_material.models import RawInwardMaterial, RawInwardMaterialSub,RmMaterialIssue,RmMaterialIssueSub
from packing_materials.models import PackingInwardMaterialSub, pmmaterialissuesub
from finished_goods.models import FGInwardMaterialSub, PackingSlipItem

class StockStatement(models.Model):
    CATEGORY_CHOICES = [
        ('RM', 'Raw Materials'),
        ('PM', 'Packing Materials'),
        ('FG', 'Finished Goods'),
    ]
    
    product_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='RM')
    inward = models.PositiveIntegerField(default=0)
    outward = models.PositiveIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)
    order_level = models.PositiveIntegerField(default=0)
    open_balance = models.PositiveIntegerField(default=0)
    closing_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product_name} - {self.get_category_display()} - Balance: {self.balance}"

    def update_stock(self):
        """Fetch stock data from Raw Materials (RM), Packing Materials (PM), and Finished Goods (FG)"""
        
        raw_inward = raw_outward = pm_inward = pm_outward = fg_inward = fg_outward = 0

        if self.category == "RM":
            raw_inward = RawInwardMaterialSub.objects.filter(material__name=self.product_name).aggregate(Sum('quantity'))['quantity__sum'] or 0
            raw_outward = RmMaterialIssueSub.objects.filter(material__name=self.product_name).aggregate(Sum('quantity'))['quantity__sum'] or 0

        elif self.category == "PM":
            pm_inward = PackingInwardMaterialSub.objects.filter(material__name=self.product_name).aggregate(Sum('quantity'))['quantity__sum'] or 0
            pm_outward = pmmaterialissuesub.objects.filter(material__name=self.product_name).aggregate(Sum('quantity'))['quantity__sum'] or 0

        elif self.category == "FG":
            fg_inward = FGInwardMaterialSub.objects.filter(material__name=self.product_name).aggregate(Sum('quantity'))['quantity__sum'] or 0
            fg_outward = PackingSlipItem.objects.filter(product__name=self.product_name).aggregate(Sum('quantity'))['quantity__sum'] or 0

        self.inward = raw_inward + pm_inward + fg_inward
        self.outward = raw_outward + pm_outward + fg_outward
        self.balance = self.inward - self.outward
        self.open_balance = self.inward - self.outward
        self.closing_stock = self.balance
        self.reorder_level = max(self.outward - self.inward, 0)
        self.order_level = self.reorder_level * 1.5
        self.save()
