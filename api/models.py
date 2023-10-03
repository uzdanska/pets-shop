from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname_lastname = models.CharField(max_length = 100, null=True)
    is_client = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='products/image')
    thumbnail = models.ImageField(upload_to='products/thumbnail')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        if self.thumbnail:
            image = Image.open(self.thumbnail.path)
            max_width = 200
            print(image.width)
            if image.width > max_width:
                w_percent = max_width / float(image.width)
                h_size = int(float(image.height) * float(w_percent))
                image.thumbnail((max_width, h_size))
                image.save(self.thumbnail.path)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shippingAddress = models.TextField()
    orderItems = models.ManyToManyField(OrderItem)
    orderDate = models.DateTimeField(auto_now_add=True)
    paymentDue = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'
    
    def get_total_price(self):
        total = 0
        for item in self.orderItems.all():
            total += item.get_total_price()
        return total
    




