from django.contrib import admin
from .models import Animal, MilkRecord, Sale, Expense, FeedStock, FeedUsage

# Base class to make a model read-only in admin
class ReadOnlyAdmin(admin.ModelAdmin):
    # make all fields read-only
    readonly_fields = [f.name for f in admin.ModelAdmin.model._meta.get_fields()]
    
    # disable add, delete, and change permissions
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

# Register models with the ReadOnlyAdmin
admin.site.register(Animal, ReadOnlyAdmin)
admin.site.register(MilkRecord, ReadOnlyAdmin)
admin.site.register(Sale, ReadOnlyAdmin)
admin.site.register(Expense, ReadOnlyAdmin)
admin.site.register(FeedStock, ReadOnlyAdmin)
admin.site.register(FeedUsage, ReadOnlyAdmin)




