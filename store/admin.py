from django.contrib import admin

from .models import Product,Orderitem,Order,BillingAddress,Orderadd

# Register your models here.

admin.site.register(Product)
admin.site.register(Orderitem)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Orderadd)
