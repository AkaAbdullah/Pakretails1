from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from .models import OrderPlaced, Product
from .models import Cart
from .models import Customer
from .models import Feedback
from django.views import View
from .forms import CustomerRegistrationForm,AddressForm, FeedBackForm,OrderPlacedForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def home(request):
    products= Product.objects.all()
    return render(request,'mainpage/home.html',{'products':products})


class CustomerRegistrationView(View):
    def get(self,request):
        form =CustomerRegistrationForm()
        return render(request,'mainpage/signup.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        message=messages.success(request,'Account Created Suuccessfully!')
        return redirect('login_user')

@login_required
def profile(request):
    return render(request,'mainpage/profile.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product= Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart =Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
        return render(request,'mainpage/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart= Cart.objects.filter(user=user)
        amount =0
        shipping_amount =150
        total_amount =0
        cart_product =[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request,'mainpage/cartpage.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'mainpage/emptycart.html')

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0
        shipping_amount = 150
        cart_product =[p for p in Cart.objects.all() if p.user== request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data={
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0
        shipping_amount = 150
        cart_product =[p for p in Cart.objects.all() if p.user== request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data={
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0
        shipping_amount = 150
        cart_product =[p for p in Cart.objects.all() if p.user== request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data={
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def checkout(request):
    user=request.user
    add= Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0
    shipping_amount = 150
    total_amount = 0
    cart_product =[p for p in Cart.objects.all() if p.user== request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount= amount+shipping_amount
    fm=OrderPlacedForm()
    return render(request,'mainpage/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'fm':fm})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self,request):
        form = AddressForm()
        details=Customer.objects.filter(user=request.user)
        return render(request,'mainpage/address.html',{'form':form,'details':details})
    def post(self,request):
        form=AddressForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['fullname']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            address=form.cleaned_data['address']
            email=form.cleaned_data['email']
            phone_no=form.cleaned_data['phone_no']
            reg =Customer(
                user=usr,
                fullname=name,
                city=city,
                state=state,
                address=address,
                email=email,
                phone_no=phone_no
            )
            reg.save()
            messages.success(request,'Address Added Successfully')
        return render(request,'mainpage/address.html')
@login_required
def deliveryaddress(request):
    delivery = Customer.objects.filter(user=request.user)
    return render(request,'mainpage/deliveryaddress.html',{'delivery':delivery})

def about(request):
    return render(request,'mainpage/about.html')

@method_decorator(login_required, name='dispatch')
class FeedbackView(View):
    def get(self,request):
        form = FeedBackForm()
        return render(request, 'mainpage/feedback.html',{'form':form})
    def post(self,request):
        if request.user.is_authenticated:
            form=FeedBackForm(request.POST)
            if form.is_valid():
                usr=request.user
                message=form.cleaned_data['message']
                reg= Feedback(user=usr,message=message)
                reg.save()
                messages.success(request,'Thank You for the Feedback :)')
                return render(request,'mainpage/feedback.html')
        else:
            return redirect('login_user')
def paymentmethod(request):
    user=request.user
    custid =request.GET.get('custid')
    paymentmethod = request.GET.get('paymentmethod')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,paymentmethod=paymentmethod).save()
        c.delete()
    return render(request, 'mainpage/paymentmethod.html')

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request,'mainpage/orders.html',{'order_placed':op})