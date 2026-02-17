from django.contrib import admin
from .models import Animal, MilkRecord, Sale, Expense, FeedStock, FeedUsage

# Base class to make a model read-only
class ReadOnlyAdmin(admin.ModelAdmin):
    # override get_readonly_fields per model
    def get_readonly_fields(self, request, obj=None):
        # get all field names for the model
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Register models with ReadOnlyAdmin
admin.site.register(Animal, ReadOnlyAdmin)
admin.site.register(MilkRecord, ReadOnlyAdmin)
admin.site.register(Sale, ReadOnlyAdmin)
admin.site.register(Expense, ReadOnlyAdmin)
admin.site.register(FeedStock, ReadOnlyAdmin)
admin.site.register(FeedUsage, ReadOnlyAdmin)
