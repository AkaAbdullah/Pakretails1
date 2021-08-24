from django.contrib.auth.models import User
from django.db import models
from rest_framework import fields, serializers
from .models import  OrderPlaced


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPlaced
        fields = ['id','user','fullname','product','quantity','ordered_date','city','state','delivery_address','email','contact','status','paymentmethod','amount']