from django.shortcuts import render,HttpResponse,redirect
from .models import Category,Product,Cart,CartItem,Order,OrderItem
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
from django.contrib.auth.models import User,Group
from django.contrib.auth import login , authenticate
from .forms import SignUpform
from django.contrib.auth.forms import AuthenticationForm

def home(request,category_slug=None):
    category_page = None
    product = None
    if category_slug != None :
        category_page = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(Category=category_page,avilable=True)
    else:
        products = Product.objects.all().filter(avilable=True)
    return render(request , "store/home.html" , {"Category":Category , "products":products })

def product_page(request , category_slug , product_slug):
    try:
        product = Product.objects.get(slug=product_slug , Category__slug = category_slug)
    except Exception as e:
        raise e
        
    return render(request,"store/product.html" , {"product" : product})


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < product.stock:  # بررسی موجودی کالا
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart, 
            quantity=1,  # مقدار اولیه را ۱ قرار می‌دهیم
        )
        cart_item.save()
    
    return redirect('cart_detail')
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Store - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        try:
            print(f"dddd")
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )

            # Creating the order
            try:
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )
                order_details.save()
                for order_item in cart_items:
                    or_item = OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )
                    or_item.save()

                    # reduce stock
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    
                    order_item.delete()
                    
                return redirect('home')      
        
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return False, e
	    
    return render(request, 'store/cart.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description))

def removed(request, product_id):
    cart_id = _cart_id(request)
    try:
        cart = Cart.objects.get(cart_id=cart_id)
        product = Product.objects.get(id=product_id)  # دریافت محصول
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # حذف آیتم اگر تعداد آن برابر 1 باشد

    except Cart.DoesNotExist:
        # در صورت عدم وجود سبد خرید
        pass
    except Product.DoesNotExist:
        # در صورت عدم وجود محصول
        pass
    except CartItem.DoesNotExist:
        # در صورت عدم وجود آیتم در سبد خرید
        pass

    return redirect('cart_detail')
def cart_remove_product(request,product_id):
    cart =Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart_detail')
def SignUpview(request):
    form = SignUpform()
    if request.method == 'POST':
        form = SignUpform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customers')
            customer_group.user_set.add(signup_user)
            login(request,signup_user)
    else:
        form = SignUpform()
    return render(request,'store/signup.html',{'form':form})

def signinview(request):
    if request.method =='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if User is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request,'store/signin.html',{"form":form})
