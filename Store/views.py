import razorpay
from . import forms
from . import models
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import razorpay
import string
import random



# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import asyncio


deliveryCharge =0
MIN_AMOUT_ORDER = 50


def Signout(request):
    logout(request)
    return redirect("homepage")
# Create your views here.


class HomePage(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        category = models.Category.objects.all()
        products = self.getProducts(category)
        return render(request, "store/Homepage.html", {"products":products, "categories":category,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

    def getProducts(self, category):
        products = []
        for category_name in category:
            p = models.Product.objects.filter(product_ctgry = category_name)
            products.extend(p)
        return products


class ProfilePage(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        if request.user.is_authenticated:
            c = models.Customer.objects.get(user__id = request.user.id)
            editForm = forms.UserEditForm(data={"email":request.user.username,"full_name":request.user.first_name, "phone":c.number, "address":c.address})
            return render(request, "store/profile.html", {"editForm":editForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})
        else:return redirect("loginpage")

    def post(self, request):
        if request.user.is_authenticated:

            form = forms.UserEditForm(data=request.POST)
            if form.is_valid():
                User.objects.filter(username=request.user.username).update(
                    first_name= form.cleaned_data["full_name"]
                )
                models.Customer.objects.filter(user__id = request.user.id).update(
                    number=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                )
                return render(request, "store/profile.html", {"editForm":form,"profileUpdated":True, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
            else:
                return render(request, "store/profile.html", {"editForm":editForm, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
        else:return redirect("loginpage")

class LoginPage(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        loginForm = forms.LoginForm()
        return render(request, "store/login.html", {"loginForm":loginForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

    def post(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
        # print(form.errors)
        form.add_error("password", "Invalid email/password.")
        return render(request, "store/login.html", {"loginForm":form,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})


class RegisterUser(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        registerForm = forms.RegisterForm()
        return render(request, "store/register.html", {"registerForm":registerForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

    def post(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        regForm = forms.RegisterForm(request.POST)
        if regForm.is_valid():
            user = User.objects.create(
                username= regForm.cleaned_data["email"],
                first_name= regForm.cleaned_data["name"],
                email= regForm.cleaned_data["email"],
            )
            user.set_password(regForm.cleaned_data["password"])
            user.save()
            customer = models.Customer.objects.create(
                user= user,
                number=regForm.cleaned_data["phone"],
                address= regForm.cleaned_data["address"]
            )

            login(request, user)
            return redirect("homepage")

        else:return render(request, "store/register.html", {"registerForm":regForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})



@login_required
def CartPage(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    # if request.method == "POST":
    products = []
    total = deliveryCharge
    try:
        cartItems = request.POST["cartInput"]
        for pid, qtty in  json.loads(cartItems).items():
            p = models.Product.objects.get(id=int(pid))
            products.append((p,qtty))
            total += (p.price*qtty)
        request.session["payment"] = cartItems

        customer = models.Customer.objects.get(user__id=request.user.id)
        return render(request, "store/cart.html", {"products":products, "deliveryCharge":deliveryCharge,"total":total,"customer":customer,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})
    except:
        return render(request, "store/cart.html", {"cartEmpty":True, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})



class Payment(View):
    def post(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()

        againPhone = request.POST["againPhone"]
        againAddress = request.POST["againAddress"]
        paymentmethod = request.POST["paymentmethod"]

        customer = models.Customer.objects.get(user__id=request.user.id)
        if againAddress == customer.address:
            againAddress = ''
        if againPhone == customer.number:
            againPhone = ''
        # product info
        amount = deliveryCharge
        item_x_quantity = ""
        cartItems = request.session["payment"]
        for pid, qtty in  json.loads(cartItems).items():
            p = models.Product.objects.get(id=int(pid))
            amount += (p.price*qtty)

            item_x_quantity += f"{p.name} x {p.price}, "

        if amount < 50:
            return redirect( to="cartpage", permanent=True)


        order_id = 'SCTXN' + str(random.randrange(100, 100000))+random.choice(string.ascii_letters)+ str(random.randrange(100, 100000))+ random.choice(string.ascii_letters)

        order = models.Orders.objects.create(
            user = User.objects.get(id=request.user.id),
            products_info =cartItems,
            againPhone= againPhone,
            againAddress= againAddress,
            amount=amount,
        )

        if paymentmethod == "cod":
            order.txn_status = "cod"
            order.razorpay_order_id = order_id
            order.order_status="active"
            order.save()

            address = request.user.first_name +", " + customer.number +", " + customer.address

            # channel_layer = get_channel_layer()
            # print(channel_layer.group_name)
            order_details = {
                "name": request.user.first_name,
                "number": customer.number if customer.number else againPhone,
                "address": customer.address if customer.address else againAddress,
                "amount":amount,
                "item_x_quantity": item_x_quantity,
                "status": order.order_status,
                "payment": order.txn_status ,
                "placed_at": order.time.strftime(r"%b. %d, %Y, %I:%M %p"),
                "order_id": order.id,
            }
            # async_to_sync(channel_layer.group_send)("counter",{"type":'send_notification',"message":json.dumps(order_details)})

            return render(request, "store/paymentsuccess.html",{"COD":True, "orderid":order.razorpay_order_id, "address":address,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

        else:
            client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            data = {"amount": amount*100, "currency": "INR", "receipt": order_id}
            razor_order  = client.order.create(data=data)
            razor_order_id = razor_order["id"]
            razor_order_reciept = razor_order["receipt"]

            payment = {
                "keyid":settings.KEY_ID,
                "id": razor_order_id,
                "shopname":"Nani Ke Samose",
                "currency":"INR",
                "amount":amount*100,
                "url":"../../handlepayment/",
                "name":customer.user.first_name,
                "email":customer.user.email,
                "number":customer.number,
            }

            order.razorpay_order_id= razor_order_id
            order.razorpay_order_reciept= razor_order_reciept
            order.payment_method = "online"
            order.save()
            return render(request, "store/payment_processing.html",{"payment":payment, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})

@csrf_exempt
def paymenthandler(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            razorpay_client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                models.Orders.objects.filter(razorpay_order_id=razorpay_order_id).update(
                    txn_status='paid',
                    order_status="active",
                    razorpay_signature=signature,
                    razorpay_payment_id=payment_id
                )
                c = models.Customer.objects.get(user__id=request.user.id)
                address = request.user.first_name +", " + c.number +", " + c.address
                return render(request, 'store/paymentsuccess.html',{"orderid":razorpay_order_id,"transactionid":payment_id, "address":address, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
            else:
                models.Orders.objects.filter(razorpay_order_id=razorpay_order_id).update(
                    txn_status='failed',
                    razorpay_signature=signature,
                    razorpay_payment_id=payment_id
                )
                return render(request, 'store/paymentfail.html',{"orderid":razorpay_order_id, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
        except Exception as e:
            print(e)
            return render(request, 'store/orderfailed.html',{"orderid":razorpay_order_id, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})




def AboutPage(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    return render(request, "store/about.html", {"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

@csrf_exempt
def ManageSessionCart(request, action):
    print(action)
    pid = request.POST["id"]
    try:
        cart = request.session["cart"]
    except:
        cart = request.session["cart"] = {}
    # adding item to cart
    item = cart.get(pid)
    if item is None:
        cart[pid] = 1 # { pid:qtty }
    else:
        prev_qtty = cart[pid]
        cart[pid] = prev_qtty + 1

    request.session["cart"] = cart
    return HttpResponse("ok")



@login_required(redirect_field_name="loginpage")
def UserOrders(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    if request.method == "GET":
        user_orders = []
        o = models.Orders.objects.filter(user__id  = request.user.id).order_by("-time")
        for order in o:
            temp = [order, ]
            o_array = []
            for pid,qtty in json.loads(order.products_info).items():
                p = models.Product.objects.get(id=pid)
                o_array.append( ( p, qtty) )
            temp.append(o_array)
            user_orders.append(temp)
            # temp.extend([order,])
        return render(request, 'store/orders.html', {"orders":user_orders, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
