from django.contrib import admin
from transactions.models import Transaction,Creditcard
# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user','receiver','status']

class CreditcardAdmin(admin.ModelAdmin):
    list_display = ['user','number','cvv','card_type']


admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Creditcard,CreditcardAdmin)