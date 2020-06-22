from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,name="Home"),
    path('cart/', views.cart,name="Cart"),
    path('checkout/', views.checkout,name="Checkout"),
    path('register/', views.register,name="Register"),
    path('login/', views.Login,name="Login"),
    path('logout/',views.Logout,name="Logout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('search/',views.search,name="search")
]

