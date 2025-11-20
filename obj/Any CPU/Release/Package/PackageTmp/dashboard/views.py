from django.shortcuts import render
from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from decimal import Decimal, InvalidOperation
 
from master.models import ItemDetail, BillOfMaterials
from raw_material.models import RawInwardMaterialSub, RmMaterialIssueSub
from finished_goods.models import FGInwardMaterialSub, PackingSlipItem
from packing_materials.models import PackingInwardMaterialSub, pmmaterialissuesub


def dashboard_view(request):
    stock_chart_data = []
 
    inward_items = ItemDetail.objects.filter(
        Q(item_code__in=RawInwardMaterialSub.objects.values('item_code')) |
        Q(item_code__in=FGInwardMaterialSub.objects.values('item_code')) |
        Q(item_code__in=PackingInwardMaterialSub.objects.values('item_code'))
    ).distinct()
 
    for item in inward_items:
        item_code = item.item_code
        item_name = item.item_name
        category = item.category.name if item.category else "Unknown"
 
        inward_raw = RawInwardMaterialSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']
        inward_fg = FGInwardMaterialSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']
 
        inward_pm = PackingInwardMaterialSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']
 
        total_inward_stock = inward_raw + inward_fg + inward_pm
 
        issued_rm = RmMaterialIssueSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']
 
        issued_fg = PackingSlipItem.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('qty', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']

        issued_pm = pmmaterialissuesub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']
 
        bom_rm_deduction = Decimal(0)
        bom_pm_deduction = Decimal(0)
 
        bom_fg_entries = BillOfMaterials.objects.filter(item_code=item_code)
        for bom in bom_fg_entries:
            try:
                required_qty = Decimal(bom.required_qty)
            except (TypeError, ValueError, InvalidOperation):
                required_qty = Decimal(0)
 
            fg_produced_qty = FGInwardMaterialSub.objects.filter(item_code=bom.item.item_code).aggregate(
                total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
            )['total']
 
            deduction = required_qty * fg_produced_qty
 
            if category == "Raw Material":
                bom_rm_deduction += deduction
            elif category == "Packing Material":
                bom_pm_deduction += deduction
 
        total_issued_stock = issued_rm + issued_fg + issued_pm + bom_rm_deduction + bom_pm_deduction
 
        calculated_stock = total_inward_stock - total_issued_stock
        closing_stock = calculated_stock if calculated_stock > 0 else Decimal('10.00')


 
        stock_chart_data.append({
            'item_name': item_name,
            'category': category,
            'inward': float(total_inward_stock),
            'issued': float(total_issued_stock),
            'closing': float(closing_stock)
        })
 
    return render(request, 'dashboard/dashboard.html', {
        'stock_chart_data': stock_chart_data
    })


