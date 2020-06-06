from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,View,DetailView
from .models import Product,Order,Orderitem,BillingAddress,Orderadd
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from django.db.models import Q


from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = 'g03aveWsb61V@M&w'


# Create your views here.


def header(request):
    order = Order.objects.filter(items)
    qs=order.count()
    context={'qs':qs}
    return render(request,'header.html',context)


class HomeView(ListView):
    model = Product
    template_name='index.html'


def search(request):
    if request.method == "POST":
        try:
            q=request.POST.get('q')
        except:
            q=None
        if q:
            products=Product.objects.filter(product_name__icontains=q)
            context={'query':q,'products':products}
            template='search.html'
        else:
            template='index.html'
            context={}
        return render(request,template,context)
    return HttpResponse("/")

    
class ProductView(DetailView):
    model=Product
    template_name='product-detail.html'

def checkout(request):
    context = {
            'order':Order.objects.get()
        }
    if request.method == "POST":
    #print(request)
       # amount=request.POST.get('amount','')
        name = request.POST.get('name','')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orderadd(name=name, email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        order.save()
        id=order.order_id
        print(id)
        order = Order.objects.get()
        amount=order.get_total()
        print(amount)
        param_dict={
            'MID': 'aWRylh81879830028261',
            'ORDER_ID': str(id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request,'paytm.html',{'param_dict':param_dict})
    return render(request,'checkout.html',context)


@csrf_exempt
def handlerequest(request):
    #paytm will send post request here
    form=request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i == 'CHECKSUMHASH':
            checksum=form[i]
    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful beacause'+response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response':response_dict})



class CheckoutView(View):
    def get(self,*args,**kwargs):
        order=Order.objects.get()
        form=CheckoutForm()
        context={
            'form':form,
            'order':order
        }
        return render(self.request,"checkout.html",context)
    def post(self,*args,**kwargs):
        form=CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                street_address=form.cleaned_data.get('street_address')
                apartment_address=form.cleaned_data.get('apartment_address')
                country=form.cleaned_data.get('country')
                zip=form.cleaned_data.get('zip')
                #add functionality AFTER ON FIELD
                #same_shipping_addess=form.cleaned_data.get('same_shipping_addess')
                #save_info=form.cleaned_data.get('save_info')
                #payment_option=form.cleaned_data.get('payment_option')
                billing_address=BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                amount=order.get_total()
                print(amount)
                billing_address.save()
                order.billing_address=billing_address
                return redirect('store:checkout')
            messages.warning(self.request,"failed checkout")
            return redirect('store:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have active order")
            return redirect("store:checkout")
            #print(form.cleaned_data)
            #print("the form is valid")
    
class OrderSummaryView(View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            return render(self.request,'shoping-cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have active order")
            return redirect("/")      




def add_to_cart(request,slug):
    
    item = get_object_or_404(Product,slug=slug)
    order_item, created = Orderitem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request,"This Item Quantity was Updated ")
            return redirect("store:order-summary")
        else:
            messages.info(request,"This Item was Added to your Cart")
            order.items.add(order_item)
            return redirect("store:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This Item was Added to your Cart")
        return redirect("store:order-summary")

def remove_from_cart(request,slug):
    
    item = get_object_or_404(Product,slug=slug)

    order_qs = Order.objects.filter(
    #check if order item is in order
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Orderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"this Item was Remove from your Cart")
            return redirect("store:order-summary")
        else:
            messages.info(request,"this Item was not in your Cart")
            return redirect("store:order-summary")
    else:
        messages.info(request,"You do not have an active order")
        #add msg saying the user doesnot have an order 
        return redirect("store:order-summary")    
    return redirect("store:order-summary")
    


def remove_single_item_from_cart(request,slug):
    
    item = get_object_or_404(Product,slug=slug)

    order_qs = Order.objects.filter(
    #check if order item is in order
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Orderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity-=1
                order_item.save()
            else:
                order.items.remove(order_item)
           
            messages.info(request,"this Item Quantity was Updated")
            return redirect("store:order-summary")
        else:
            messages.info(request,"this Item was not in your Cart")
            return redirect("store:product",slug=slug)
    else:
        messages.info(request,"You do not have an active order")
        #add msg saying the user doesnot have an order 
        return redirect("store:product", slug=slug)    
    return redirect("store:product", slug=slug)
    

def blog(request):
    return render(request,'blog.html')


def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')