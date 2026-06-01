from django.db import models

from products.models import Product


class Inventory(models.Model):

    # Product Connection

    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE

    )

    # Available Stock

    stock = models.IntegerField()

    # Low Stock Alert Limit

    low_stock_threshold = models.IntegerField(

        default=5

    )

    # Auto Update Time

    last_updated = models.DateTimeField(

        auto_now=True

    )

    # Display Name in Admin Panel

    def __str__(self):

        return self.product.name


class StockHistory(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    action = models.CharField(max_length=50)  # e.g., 'Added', 'Updated', 'Sold', 'Returned'

    quantity = models.IntegerField()  # e.g., +20, -5

    status = models.CharField(max_length=50)  # e.g., 'In Stock', 'Low Stock', 'Out Of Stock'

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f"{self.product.name} - {self.action} ({self.quantity}) at {self.timestamp}"