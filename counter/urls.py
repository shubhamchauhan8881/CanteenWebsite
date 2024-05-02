
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="counterhome"),
    path('logout/', views.Signout),
    path('login/', views.CounterManLogin, name="counterlogin"),
    path('all/', views.AllOrders),
    path('completed/', views.Completedrders),
    path('failed/', views.FailedOrders),
    path('accepted/', views.AcceptedOrder),
    path('rejected/', views.RejectedOrder),
    path('setstatus/<str:status>/', views.SetOrderStatus),
    path('notification/', views.NotificationAJAX)
]
