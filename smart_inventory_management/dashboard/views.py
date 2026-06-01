import datetime

from django.shortcuts import render

from django.db.models import Sum, F, Count

from products.models import Product

from sales.models import Sale

from inventory.models import Inventory


def dashboard(request):

    # CURRENT DATE

    today = datetime.date.today()

    current_month = today.month

    current_year = today.year


    # =========================================
    # TOTAL PRODUCTS
    # =========================================

    total_products = Product.objects.count()


    # =========================================
    # MONTHLY SALES
    # =========================================

    sales_this_month = Sale.objects.filter(

        created_at__month=current_month,

        created_at__year=current_year

    )

    total_sales = sales_this_month.count()


    # =========================================
    # MONTHLY REVENUE
    # =========================================

    monthly_revenue = sales_this_month.aggregate(

        total=Sum('total_price')

    )['total'] or 0


    # =========================================
    # LOW STOCK ITEMS
    # =========================================

    low_stock_items = Inventory.objects.filter(

        stock__lte=F('low_stock_threshold'),

        stock__gt=0

    )

    low_stock_count = low_stock_items.count()


    # =========================================
    # OUT OF STOCK ITEMS
    # =========================================

    out_stock_items = Inventory.objects.filter(

        stock=0

    )

    out_stock_count = out_stock_items.count()


    # =========================================
    # TOTAL INVENTORY VALUE
    # =========================================

    total_inventory_value = 0

    inventories = Inventory.objects.select_related(

        'product'

    )

    for item in inventories:

        total_inventory_value += (

            item.stock * item.product.price

        )


    # =========================================
    # LOW STOCK ALERTS
    # =========================================

    low_stock_alerts = low_stock_items[:5]


    # =========================================
    # MONTHLY SALES ANALYTICS
    # =========================================

    chart_data = []

    for i in range(5, -1, -1):

        target_month = current_month - i

        target_year = current_year

        while target_month <= 0:

            target_month += 12

            target_year -= 1


        month_sales = Sale.objects.filter(

            created_at__month=target_month,

            created_at__year=target_year

        )


        revenue = month_sales.aggregate(

            total=Sum('total_price')

        )['total'] or 0


        month_name = datetime.date(

            target_year,

            target_month,

            1

        ).strftime('%b')


        chart_data.append({

            'month': month_name,

            'revenue': float(revenue),

        })


    # =========================================
    # DYNAMIC GRAPH HEIGHT
    # =========================================

    max_rev = max(

        [x['revenue'] for x in chart_data]

    ) if chart_data else 0


    for data in chart_data:

        if max_rev > 0:

            if data['revenue'] > 0:

                data['height'] = max(

                    int(

                        (data['revenue'] / max_rev) * 220

                    ),

                    60

                )

            else:

                data['height'] = 20

        else:

            data['height'] = 20


    # =========================================
    # SMART STOCK PREDICTIONS
    # =========================================

    stock_predictions = []

    for item in inventories:

        # IGNORE OUT OF STOCK

        if item.stock <= 0:

            continue


        # SIMPLE PREDICTION MODEL

        estimated_days = item.stock // 5


        # STATUS

        if estimated_days <= 5:

            prediction_status = "Critical"

        elif estimated_days <= 15:

            prediction_status = "Medium"

        else:

            prediction_status = "Safe"


        stock_predictions.append({

            'product': item.product.name,

            'stock': item.stock,

            'days_left': estimated_days,

            'status': prediction_status

        })

# =========================================
# BEST SELLING PRODUCT
# =========================================

    best_selling = Sale.objects.values(
        'product__name'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by(
        '-total_sold'
    ).first()

    if best_selling:
        best_product_name = best_selling['product__name']
        best_product_sales = best_selling['total_sold']
    else:
        best_product_name = "No Sales Yet"
        best_product_sales = 0

    # =========================================
    # CONTEXT
    # =========================================

    context = {

    'total_products': total_products,

    'total_sales': total_sales,

    'monthly_revenue': monthly_revenue,

    'low_stock_count': low_stock_count,

    'out_stock_count': out_stock_count,

    'total_inventory_value': total_inventory_value,

    'low_stock_alerts': low_stock_alerts,

    'chart_data': chart_data,

    'stock_predictions': stock_predictions,

    'best_product_name': best_product_name,

    'best_product_sales': best_product_sales,

}


    return render(

        request,

        'dashboard.html',

        context

    )