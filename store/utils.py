from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

def cookieCart(request):
	# cookie was deleted so create dummy cookie
	try:    
		# parse cookie string to dict format
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		
	print("\n\n cart",cart)
	items = []
	order = {'get_cart_items':0,'get_cart_total':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for item in cart:
		try:
			cartItems += cart[item]["quantity"]

			product = Product.objects.get(id=item)
			total = (product.price * cart[item]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[item]['quantity']

			item = {
				'product' :{
					'id' : product.id,
					'name' : product.name,
					'price' : product.price,
					'imageURL' : product.imageURL,
				},
				'quantity' : cart[item]['quantity'],
				'get_total' : total
			}
			items.append(item)
			if product.digital == False:
				order['shipping'] = True
		except:
			pass
	return {'cartItems' : cartItems, 'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	return {'cartItems' : cartItems, 'order':order, 'items':items}