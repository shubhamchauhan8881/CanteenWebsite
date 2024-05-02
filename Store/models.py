from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=12)
    address = models.CharField(max_length=300, default='', null=True, unique=False)
    alternate_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name





class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    product_ctgry = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True, max_length=300)
    image = models.ImageField(upload_to="uploads/products/")
    offer_discounts = models.IntegerField(default=0)
    availibility = models.BooleanField(default=True)

    last_modified = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qtty = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products_info = models.CharField(max_length=1000, null=True, blank=True)

    payment_method = models.CharField(max_length=200, default='cod')
    txn_status = models.CharField( max_length=20, default='unpaid')
    order_status = models.CharField( max_length=20, default='pending')

    againPhone = models.CharField(max_length=12)
    againAddress = models.CharField(max_length=300)

    amount = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_reciept = models.CharField(max_length=100, null=True, blank=True)
    
    razorpay_payment_id  = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=800, null=True, blank=True)


    # for notification purposes....
    is_notified = models.BooleanField(default=False)

    @staticmethod
    def get_orders_by_status(status):
        return Orders.objects.filter(order_status=status)


class NewInTheMenu(models.Model):
    name = models.ManyToManyField(to=Product)

    def __str__(self):
        return "NEW"
