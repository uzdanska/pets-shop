from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class UserProfile(models.Model):
    """
    Model representing user profile information.
    
    Fields:
        user (OneToOneField): A reference to the User model using a one-to-one relationship.
        firstname_lastname (CharField): User's first name and last name, stored as a string with a maximum length of 100 characters.
        is_client (BooleanField): Indicates whether the user is a client. Default is False.
        is_seller (BooleanField): Indicates whether the user is a seller. Default is False.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname_lastname = models.CharField(max_length = 100, null=True)
    is_client = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the string representation of the UserProfile object.
        It returns the username of the associated User object.
        """
        return self.user.username

class Category(models.Model):
    """
    Model representing Category name.

    Fields:
        name (CharField): Category's name, with string maximum length of 100 characters.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """
        Returns the string representation of the Category object.
        It returns the name of the associated Category object.
        """
        return self.name


class Product(models.Model):
    """
    Model representing Product name.

    Fields:
        name (CharField): The name of the product, with a maximum length of 200 characters. Cannot be null.
        description (TextField): A detailed description of the product. Cannot be null.
        price (DecimalField): The price of the product, represented as a decimal with a maximum of 6 digits and 2 decimal places. Cannot be null.
        category (ForeignKey): A reference to the Category model using a foreign key relationship. The product belongs to a specific category. Cannot be null.
        image (ImageField): The main image of the product, uploaded to the 'products/image' directory.
        thumbnail (ImageField): A thumbnail image of the product, uploaded to the 'products/thumbnail' directory.
    """
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
    """
    Model representing an item in the order.
    
    Fields:
        product (ForeignKey): A reference to the Product model using a foreign key relationship. The item is associated with a specific product. Cannot be null.
        quantity (PositiveIntegerField): The quantity of the product in the order.
        ordered (BooleanField): A flag indicating whether the product has been ordered or not. Default is False.

    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    """
    Model representing an order in the e-commerce system.

    Fields:
        customer (ForeignKey): A reference to the User model using a foreign key relationship. The customer who placed the order. Cannot be null.
        shippingAddress (TextField): The address where the order will be shipped. Cannot be null.
        orderItems (ManyToManyField): A list of order items associated with this order.
        orderDate (DateTimeField): The date and time when the order was placed. Automatically set to the current date and time when the order is created.
        paymentDue (DateTimeField): The deadline for payment of the order. Can be null.
        ordered (BooleanField): A flag indicating whether the order has been placed or not. Default is False.
    """
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
    




