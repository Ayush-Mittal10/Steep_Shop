from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='products/')
    size = models.CharField(max_length=50, choices=(('small','250 g'), ('medium','500 g'), ('large','1 Kg')), default='medium')
    mrp = models.IntegerField()
    price = models.IntegerField()
    product_desc = models.TextField()
    publish_date = models.DateField()
    stock = models.IntegerField()
    
    def __str__(self) -> str:
        return self.product_name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, choices=(('O','Ordered'), ('f','Failed')),default="ordered")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()


class PaymentSignature(models.Model):
    order_id = models.ForeignKey(Order)
    payment_id = models.CharField()
    key_secret = models.CharField()