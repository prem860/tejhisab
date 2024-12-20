from django.contrib import admin
from .models import Transaction  # Ensure the model is imported

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'description', 'date', 'remarks', 'added_by')
    list_filter = ('type', 'date')
    search_fields = ('description',)
