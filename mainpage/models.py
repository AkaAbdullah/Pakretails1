from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
STATE_CHOICES=(
    ('Punjab','Punjab'),
    ('Sindh','Sindh'),

)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
    address =models.CharField(max_length=300)
    email =models.EmailField()
    phone_no =models.IntegerField()
    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Lamps'),
    ('C','Wearbale'),
)
class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.IntegerField()
    discounted_price =models.IntegerField()
    description = models.TextField(max_length=500)
    brand =models.CharField(max_length=100)
    category = models.CharField( choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="uploads/",default='4x4.jpg')
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICES =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('In Transit','In Transit'),
    ('Delivered','Delivered'),
    ('Cenceled','Canceled'),
)

PAYMENT_CHOICES=(
    ('Cash on Delivery','Cash on Delivery'),
    ('Visa','Visa'),
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=50,default='pending')
    paymentmethod = models.CharField(choices=PAYMENT_CHOICES,max_length=50)
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

class Feedback(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
