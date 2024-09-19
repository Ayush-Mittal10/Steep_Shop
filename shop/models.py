from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_desc = models.TextField()
    publish_date = models.DateField()

    def __str__(self) -> str:
        return self.product_name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='products/')
    size = models.CharField(max_length=50, choices=(('small','250 g'), ('medium','500 g'), ('large','1 Kg')), default='medium')
    mrp = models.IntegerField()
    price = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.product.product_name} - {self.size}'

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
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

class PaymentSignature(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    key_secret = models.CharField(max_length=100)