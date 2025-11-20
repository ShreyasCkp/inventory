from django.shortcuts import render
from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from decimal import Decimal
from master.models import ItemDetail
from raw_material.models import RawInwardMaterialSub, RmMaterialIssueSub
from finished_goods.models import FGInwardMaterialSub, PackingSlipItem
from packing_materials.models import PackingInwardMaterialSub, pmmaterialissuesub

def stock_statement(request):
    category_filter = request.GET.get('category', 'all')

    categories = {
        'raw_material': 'Raw Material',
        'packing_material': 'Packing Material',
        'finished_goods': 'Finished Goods'
    }

    inward_items = ItemDetail.objects.filter(
        Q(item_code__in=RawInwardMaterialSub.objects.values('item_code')) |
        Q(item_code__in=FGInwardMaterialSub.objects.values('item_code')) |
        Q(item_code__in=PackingInwardMaterialSub.objects.values('item_code')) 
    ).distinct()

    if category_filter in categories:
        inward_items = inward_items.filter(category__name=categories[category_filter])

    stock_data = []

    for item in inward_items:
        item_code = item.item_code
        item_name = item.item_name
        category = item.category.name if item.category else "Unknown"
        rol = item.rol or Decimal(0)
        uom = item.uom or 'units'

        inward_raw = RawInwardMaterialSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']

        inward_fg = FGInwardMaterialSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']

        inward_packing = PackingInwardMaterialSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']

        issued_rm = RmMaterialIssueSub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']

        issued_fg = PackingSlipItem.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('qty', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']

        issued_pm = pmmaterialissuesub.objects.filter(item_code=item_code).aggregate(
            total=Coalesce(Sum('quantity', output_field=DecimalField()), Value(0, output_field=DecimalField()))
        )['total']


        if category == "Raw Material":
            total_inward_stock = inward_raw
            total_issued_stock = issued_rm
        elif category == "Packing Material":
            total_inward_stock = inward_packing
            total_issued_stock = issued_pm
        elif category == "Finished Goods":
            total_inward_stock = inward_fg
            total_issued_stock = issued_fg
        else:
            total_inward_stock = Decimal(0)
            total_issued_stock = Decimal(0)

        # Safe defaults
        closing_stock = max(total_inward_stock - total_issued_stock, Decimal('10.00'))
        balance_qty = max(closing_stock + total_inward_stock - total_issued_stock, Decimal('10.00'))

        # Alert logic
        inward_less_than_issued = total_inward_stock < total_issued_stock

        if closing_stock < rol:
            alert_type = 'warning'
            status_message = "⚠️ Reorder Needed"
            needs_reorder = True
        else:
            alert_type = 'normal'
            status_message = "✅ Sufficient Stock"
            needs_reorder = False

        play_beep = needs_reorder or inward_less_than_issued

        stock_data.append({
            'item_code': item_code,
            'item_name': item_name,
            'category': category,
            'rol': f"{rol} {uom}",
            'inward_stock': f"{total_inward_stock:.2f} {uom}",
            'issued_stock': f"{total_issued_stock:.2f} {uom}",
            'closing_stock': f"{closing_stock:.2f} {uom}",
            'balance_qty': f"{balance_qty:.2f} {uom}",
            'needs_reorder': needs_reorder,
            'alert_type': alert_type,
            'play_beep': play_beep,
            'status_message': status_message,
            'highlight_issue': inward_less_than_issued
        })

    return render(request, 'stock_statement/stock_statement.html', {
        'stock_data': stock_data,
        'category_filter': category_filter,
        'categories': categories
    })


