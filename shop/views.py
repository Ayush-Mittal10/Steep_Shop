import random
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
import razorpay.errors
from shop.models import *
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.core import serializers
from shop.forms import AddToCartForm
import razorpay
from django.conf import settings
from django.utils.html import strip_tags
from django.core import mail
import hmac
import hashlib

# Create your views here.
def home(request):
    queryset = ProductVariant.objects.filter(size='medium').select_related('product')
    cart = request.session.get('cart', {})
    return render(request, "shop/home.html", {'products':queryset, 'cart':cart})

def all_products(request):
    queryset = ProductVariant.objects.filter(size='medium').select_related('product')
    cart = request.session.get('cart', {})
    return render(request, "shop/products.html", {'products':queryset, 'cart':cart})

def product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    variants = ProductVariant.objects.filter(product=product)
    print(variants)

    context = {
        'product': product,
        'variants': variants,
        'cart': request.session.get('cart', {})
    }
    products = Product.objects.all()
    form = AddToCartForm(request.POST)
    if form.is_valid():
        product_id = request.POST.get('product_id')
        quantity_change = int(request.POST.get('quantity', 0))
        cart = request.session.get('cart', {})

        if product_id:
            product_id = str(product_id)
            if product_id in cart:
                cart[product_id] += quantity_change
                if cart[product_id] <= 0:
                        del cart[product_id]
            else:
                cart[product_id] = 1 if quantity_change > 0 else 0
                request.session['cart'] = cart

        else:
            print("Error: Missing product_id in POST request")
        context = {
            'product': product,
            'products': products
        }
    return render(request, "shop/viewProduct.html", context)

class carting(View):
    def post(self, request):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = request.POST.get('product_id')
            quantity_change = int(request.POST.get('quantity', 0))
            cart = request.session.get('cart', {})

            if product_id:
                product_id = str(product_id)
                if product_id in cart:
                    cart[product_id] += quantity_change
                    if cart[product_id] <= 0:
                        del cart[product_id]
                else:
                    cart[product_id] = 1 if quantity_change > 0 else 0
                request.session['cart'] = cart

            else:
                print("Error: Missing product_id in POST request")
        return redirect('cart')

    def get(self, request):

        clear = request.GET.get('clear')
        if clear:
            request.session['cart'] = {}
            return redirect('cart')
        cart = request.session.get('cart', {})
        print(cart)
        products = ProductVariant.objects.filter(id__in=cart.keys())
        
        for product in products:
            product.quantity = cart.get(str(product.id))
        
        total_items = sum(cart.values())
        total_price = sum(product.price * quantity for product, quantity in zip(products, cart.values()))
        context = {
            'cart': cart,
            'products': products,
            'total_items':total_items,
            'amount':total_price
        }

        checkout = request.GET.get('checkout')
        if checkout:
            checkout(request, total_price)
        return render(request, 'shop/cart.html', context)

@require_POST
def update_cart(request):
    clear = request.POST.get('clear')
    
    if clear:
        request.session['cart'] = {}
        response = {'success': True}
        return JsonResponse(response)

    check = request.POST.get('check')
    cart = request.session.get('cart')
    if check and cart:
        return JsonResponse({'success': True})
    variant_id = request.POST.get('variant_id')
    quantity_change = int(request.POST.get('quantity', 0))
    buy = request.POST.get('buy')
    if buy:
        cart = {}
        cart[variant_id] = max(quantity_change, 1)
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    if not cart:
        cart = {}

    if variant_id:
        variant_id = str(variant_id)
        if variant_id in cart:
            cart[variant_id] += quantity_change
            if cart[variant_id] <= 0:
                del cart[variant_id]
        else:
            cart[variant_id] = max(quantity_change, 1)

        request.session['cart'] = cart
        products = ProductVariant.objects.filter(id__in=cart.keys())
        
        for product in products:
            product.quantity = cart.get(str(product.id))
        
        total_items = sum(cart.values())
        total_price = sum(product.price * quantity for product, quantity in zip(products, cart.values()))
        response = {
            'success': True,
            'quantity': cart.get(variant_id, 0),
            'total_items': total_items,
            'amount': total_price
            }
        
    else:
        response = {'success': False, 'error': 'Invalid product Id'}
    
    return JsonResponse(response)
    
    

def checkout(request):
    cart = request.session.get('cart')
    if not cart:
        return redirect('cart')
    payment = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        payment_method = request.POST.get('payment_method')

        request.session['name'] = first_name + ' ' + last_name
        request.session['email'] = email
        products = ProductVariant.objects.filter(id__in=cart.keys())
        amount = sum(product.price * quantity for product, quantity in zip(products, cart.values()))
        print(amount)
        print(request.session.items())

        try:
            order = Order(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                amount=amount
            )
            order.save()
            print(f"Order saved with ID: {order.order_id}")
            print(payment_method)

            for product in products:
                quantity = cart.get(str(product.id))
                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                order_item.save()
                print(f"OrderItem saved with Product ID: {product.id}")

            request.session['cart'] = {}
            if payment_method == 'online':
                amount = amount*100
                client = razorpay.Client(auth=("rzp_test_LrPemutnPTMIpm", "4R01eQ9BX6GfBXvGT0wd7vyM"))
                payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
                print(payment)
                response = {'payment': payment, 'name':first_name+" "+last_name, 'email':email, 'phone':phone, 'order_id':order.order_id}
                return JsonResponse(response)

        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'shop/checkout.html', {'error': str(e)})

    return render(request, 'shop/checkout.html')

@csrf_exempt
def success(request):
    if request.method == 'POST':
        
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        order_id = request.POST.get('order_id')
        email = request.GET.get('email')
        name = request.GET.get('name')

        print(f"Email id: {email}")
        print(f"Name: {name}")
        print(f"Order ID: {order_id}")

        if verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):

            send_mail('Order Confirmation', f"""Hi {name}, 
                    Your order with order ID: {order_id} has been placed successfully.""", 
                    settings.EMAIL_HOST_USER, [email], fail_silently=False)

            send_mail('New Order Received', f'A new order has been placed by {name}. Order Id: {order_id}',
                    settings.EMAIL_HOST_USER, ['ayushmittal0506@gmail.com'], fail_silently=False)

        return render(request, 'shop/ordered.html')

    return redirect('home')

def verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    
    try:
        client = razorpay.Client(auth=("rzp_test_LrPemutnPTMIpm", "4R01eQ9BX6GfBXvGT0wd7vyM"))
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
            })
        return True
    except razorpay.errors.SignatureVerificationError as e:
        print(f"Error: {e}")
        return False