from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .tasks import send_email
from .models import * 
from django.http import JsonResponse
import json
import datetime
from .utils import *

# Create your views here.

# def index(request):
#     if request.user.is_authenticated:
#         # create customer
#         customer, created = Customer.objects.get_or_create(
#         email = request.user.email,)
#         customer.name = request.user.username
#         customer.user = request.user
#         customer.save()
#         products = Product.objects.all()
#         customer = request.user.customer
#         # create order or if exits it will cet it 
#         order,created = Order.objects.get_or_create(customer=customer,complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items 
#     else:
#         return render(request,'store/index.html')
#     context = {'product':products,'cartItems':cartItems}
#     return render(request,'store/index.html',context)

def index(request):
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	context = {'product':products,'cartItems':cartItems}
	return render(request,'store/index.html', context)


def register(request):
	if request.method == 'POST' :
		uname = request.POST['username']
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		password = request.POST['password']
		u = User.objects.create_user(username=uname , first_name=fname , last_name=lname , email=email , password=password)
		messages.error(request,f'Account Created For {uname}!')
		if uname == uname:
			return redirect('Register')
	return render(request,'store/register.html')


def Login(request):
	if request.method == 'POST' :
		uname = request.POST['uname']
		password = request.POST['pass']
		user = authenticate(request , username=uname , password=password)
		if user is not None :
			login(request , user)
			return redirect('Home')
		else:
			messages.error(request,f'invalid user or password!')
	return render(request,'store/login.html')

@login_required
def Logout(request):
	logout(request)
	return redirect('Home')

@login_required
def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		# create order or if exits it will gcet it 
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else :
		return redirect('Home')
	context ={'items':items,'order':order,'cartItems':cartItems}
	return render(request,'store/cart.html',context)

@login_required
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		total = order.get_cart_total
		tax = 18
		tax_total = (total * tax) / 100
		grand_total = tax_total + total 
		cartItems = order.get_cart_items
	else:
		return redirect('Home')
	context ={'items':items,'order':order,'tax':tax_total,'grand_total':grand_total,'cartItems':cartItems}
	return render(request,'store/checkout.html',context)

def updateItem(request):
	# parse data
	data = json.loads(request.body)
	# query data from body and grab the value
	productId = data['productId']
	action = data['action']
	# loggedin customer
	customer = request.user.customer
	# get product
	product = Product.objects.get(id=productId)
	# get or create product
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# create order item[order is get or create]
	# if oder item already exists according to the product and order so no need to create new just 
	# change quantity add or subtract
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == "add":
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == "remove":
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse("Item was Added",safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id
		if total == float(order.get_cart_total):
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer = customer,
				order = order,
				address = data['shipping']['address'],
				city = data['shipping']['city'],
				state = data['shipping']['state'],
				country = data['shipping']['country'],
				zipcode = data['shipping']['zipcode']
			)
			send_email.delay()
	return JsonResponse('payment completed!',safe=False)

def search(request):
	query = request.GET['query']
	if len(query) > 50:
		products = []
	else:
		name = Product.objects.filter(name__icontains=query)
		price = Product.objects.filter(price__icontains=query)
		products = name.union(price)
	context = {'product':products,'query':query}
	return render(request,"store/search.html",context)

