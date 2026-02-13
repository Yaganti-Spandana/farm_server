from django.db import models
from django.contrib.auth.models import User

class Animal(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('dead', 'Dead'),
    ]

    animal_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    health_records = models.TextField()
    milk_per_day = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
    
class MilkRecord(models.Model):
    date = models.DateField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    
    morning_milk = models.FloatField()
    evening_milk = models.FloatField()
    total_milk = models.FloatField(blank=True, null=True)

    milk_home = models.FloatField(default=0)
    milk_sold = models.FloatField(default=0)
    milk_wasted = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # auto-calculate total milk
        self.total_milk = self.morning_milk + self.evening_milk
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal.name} - {self.date}"
    
class Sale(models.Model):
    date = models.DateField()
    quantity_sold = models.FloatField()   # liters
    price_per_liter = models.FloatField()
    total_income = models.FloatField(blank=True, null=True)

    buyer = models.CharField(max_length=100, blank=True, null=True)
    payment_received = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Formula: Daily Milk Income = Quantity × Price
        self.total_income = self.quantity_sold * self.price_per_liter
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.total_income}"
    
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('feed', 'Feed'),
        ('veterinary', 'Veterinary'),
        ('medicines', 'Medicines'),
        ('labor', 'Labor'),
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('equipment', 'Equipment'),
        ('animal_purchase', 'Animal Purchase'),
        ('maintenance', 'Maintenance'),
    ]

    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
class FeedStock(models.Model):
    date = models.DateField()
    feed_type = models.CharField(max_length=100)  # grass, fodder, concentrate
    quantity_in = models.FloatField()  # in kg
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.feed_type} - {self.quantity_in}kg"


class FeedUsage(models.Model):
    date = models.DateField()
    feed_type = models.CharField(max_length=100)
    quantity_used = models.FloatField()  # in kg

    def __str__(self):
        return f"{self.feed_type} used {self.quantity_used}kg"