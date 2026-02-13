from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Animal,MilkRecord,Sale,Expense,FeedStock,FeedUsage
admin.site.register(Animal)
admin.site.register(MilkRecord)
admin.site.register(Sale)
admin.site.register(Expense)
admin.site.register(FeedStock)
admin.site.register(FeedUsage)



