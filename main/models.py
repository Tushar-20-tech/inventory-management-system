from django.db import models
from django.utils import timezone


class UserProfile(models.Model):

    company_name = models.CharField(max_length=200)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    password = models.CharField(max_length=200)

    country = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    profile_image = models.ImageField(upload_to="profiles/")

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email


class Product(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    category = models.CharField(max_length=100)

    quantity = models.IntegerField()

    price = models.FloatField()

    supplier = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StockIn(models.Model):

    user = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )

    quantity_added = models.IntegerField()

    supplier = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    invoice_number = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    date = models.DateField(default=timezone.now)

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} +{self.quantity_added}"


class StockOut(models.Model):

    user = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )

    quantity_removed = models.IntegerField()

    customer = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    invoice_number = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    date = models.DateField(default=timezone.now)

    reason = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} -{self.quantity_removed}"