from master.models import ItemDetail  # Ensure you import the correct model

def fetch_item_details(stock_data):
    item_codes = stock_data.keys()
    items = ItemDetail.objects.filter(item_code__in=item_codes).values(
        "item_code", "item_name", "uom", "rate", "reorder_level"
    )

    for item in items:
        code = item["item_code"]
        if code in stock_data:
            stock_data[code]["item_name"] = item["item_name"]
            stock_data[code]["uom"] = item["uom"]
            stock_data[code]["rate"] = item["rate"]
            stock_data[code]["reorder_level"] = item["reorder_level"]



