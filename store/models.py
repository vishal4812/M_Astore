from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.

class Product(models.Model):
    product_id=models.IntegerField
    product_name=models.CharField(max_length=50)
    image=models.ImageField(default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300,default="")
    slug=models.SlugField()

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("store:product",kwargs={
            'slug':self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("store:add_to_cart",kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove_from_cart",kwargs={
            'slug':self.slug
        })



class Orderitem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    


    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(Orderitem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_total_item_price()
        return total

    def get_count(self):
        return self.items.count()

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    apartment_address=models.CharField(max_length=100)
    country=CountryField(multiple=True)
    zip=models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Orderadd(models.Model):
    order_id=models.AutoField(primary_key=True)
    #amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90,default="")
    email=models.CharField(max_length=111,default="")
    address=models.CharField(max_length=111,default="")
    city=models.CharField(max_length=111,default="")
    state=models.CharField(max_length=111,default="")
    zip_code=models.CharField(max_length=111,default="")
    phone=models.CharField(max_length=10,default="")

    def __str__(self):
        return self.name
