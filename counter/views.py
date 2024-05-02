from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from Store import models as storeModel
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User

# Create your views here.

def OrderAssembler(filters='all', by_notification = False):
    orders = []
    # [
    #     [Ordert,Customer, [ProductArray: (Product, Qtty)] ]
    # ]
    
    if by_notification:
        pp = storeModel.Orders.objects.filter(is_notified=False)
    else:
        pp = storeModel.Orders.get_orders_by_status(filters).order_by("-time") if filters != "all" else storeModel.Orders.objects.all().order_by("-time")
    
    for order in pp:
        order.is_notified=True
        order.save()

        order_array = [order, storeModel.Customer.objects.get(user = order.user)]
        products_info = json.loads( order.products_info )
        temp = []
        for pid,qtty in products_info.items():
            temp.append( (storeModel.Product.objects.get(id=pid), qtty,) )
        order_array.append(temp)
        orders.append(order_array)
    return orders

def Signout(request):
    logout(request)
    return redirect("counterhome")

def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = OrderAssembler("active")
        return render(request, 'counter/home.html',{"orders":orders})
    return redirect(reverse("counterlogin", current_app="counter"))

def Completedrders(request):
    orders = OrderAssembler("completed")
    return render(request, 'counter/completed.html',{"orders":orders})


def CounterManLogin(request):
    if request.method == "GET":
        if request.user.is_staff and request.user.is_authenticated:
            return redirect("counterhome")
        else:
            return render(request,"counter/login.html")
    else:
        email = request.POST.get('email')
        password = request.POST.get('psw')

        user = authenticate(username= email, password = password)
        if user is not None and user.is_staff:
            request.session["user"] = user.id
            login(request, user)
            return redirect("counterhome")
        else:
            return render(request, 'counter/login.html', {"err":"Invalid username or password!!"})

def AllOrders(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = OrderAssembler()
        return render(request, 'counter/all.html',{"orders":orders})
    else:
        return redirect(reverse("counterlogin", current_app="counter"))
def FailedOrders(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = OrderAssembler("failed")
        return render(request, 'counter/failed.html',{"orders":orders})
    else:
        return redirect(reverse("counterlogin", current_app="counter"))
def AcceptedOrder(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = OrderAssembler("accepted")
        return render(request, 'counter/accepted.html',{"orders":orders})
    else:
        return redirect(reverse("counterlogin", current_app="counter"))

def RejectedOrder(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = OrderAssembler("rejected")
        return render(request, 'counter/rejected.html',{"orders":orders})
    else:
        return redirect(reverse("counterlogin", current_app="counter"))

@csrf_exempt
def SetOrderStatus(request, status):
    try:
        storeModel.Orders.objects.filter(id=int(request.POST["pid"])).update(order_status=status)
        return HttpResponse({"status":"success"})
    except:
        return HttpResponse({"status":"failed"})

def NotificationAJAX(request):
    # {name, number, address, amount, itemxqtty, status, payment, placed at}
    res = OrderAssembler(by_notification=True)

    if not res == []:
        data = []
        status = 'ok'
        for obj in res:
            temp = {}
            temp["id"] = obj[0].id
            temp["name"] = obj[1].user.first_name
            temp["number"] = obj[1].number
            temp["address"] = obj[1].address
            temp["amount"] = obj[0].amount
            temp["itemxqtty"] = ",".join( f"{product.name} x {qtty}" for product,qtty in obj[2] )
            temp["status"] = obj[0].order_status
            temp["txn_status"] = obj[0].txn_status
            temp["placed_at"] = obj[0].time.strftime(r"%b. %d, %Y %I:%M, %p")

            data.append(temp)
    else:
        status = "no"
        data = {}
    return JsonResponse({"status":status, "data": data}, safe=False, )