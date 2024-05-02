
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name="homepage"),
    path('profile/', views.ProfilePage.as_view(), name="userprofile"),
    path('about/', views.AboutPage, name="aboutpage"),
    path('login/', views.LoginPage.as_view(),name="loginpage"),
    path('register/', views.RegisterUser.as_view()),
    path('logout/', views.Signout),
    path('cart/', views.CartPage, name="cartpage"),
    path('orders/', views.UserOrders),
    path('payment/', views.Payment.as_view()),
    path('set-cart/<str:action>/', views.ManageSessionCart),
    path('handlepayment/', views.paymenthandler),
]

