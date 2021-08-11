from django.contrib import admin
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    Feedback
)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','fullname','city','state','address','email','phone_no']
    list_filter = ("fullname", )
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','brand','category','product_image']
    list_filter = ("category", )
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
    list_filter = ("product", )
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['user','fullname','product','quantity','ordered_date','city','state','delivery_address','email','contact','status','paymentmethod','amount']
    list_filter = ("status", )
@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display=['id','user','message']
    list_filter = ("user", )