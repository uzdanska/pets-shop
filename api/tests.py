from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Category, Product, Order, OrderItem
import os
from PIL import Image
# Create your tests here.

class UserProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_create_user_profile(self):
        user_profile = UserProfile.objects.create(user=self.user, firstname_lastname='Test User')
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(user_profile.firstname_lastname, 'Test User')
        self.assertFalse(user_profile.is_client)
        self.assertFalse(user_profile.is_seller)

    def test_user_profile_string_representation(self):
        user_profile = UserProfile.objects.create(user=self.user, firstname_lastname='Test User')
        self.assertEqual(str(user_profile), 'testuser')

    def test_update_user_profile(self):
        user_profile = UserProfile.objects.create(user=self.user, firstname_lastname='Test User')
        user_profile.firstname_lastname = 'Updated User'
        user_profile.is_client = True
        user_profile.save()
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.firstname_lastname, 'Updated User')
        self.assertTrue(updated_profile.is_client)

    def test_delete_user_profile(self):
        user_profile = UserProfile.objects.create(user=self.user, firstname_lastname='Test User')
        user_profile.delete()
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(user=self.user)

    def test_optional_firstname_lastname_field(self):
        user_profile = UserProfile.objects.create(user=self.user)
        self.assertIsNone(user_profile.firstname_lastname)

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="test category")
    
    def test_category_name(self):
        category = Category.objects.get(id="1")
        self.assertEqual(category.name, "test category")

    def test_unique_category_name(self):
        with self.assertRaises(Exception):
            Category.objects.create(name="test category")
    
class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="test category")
        self.product = Product.objects.create(name="test name", description="test description", price=2.00, category = self.category, image='test/8in1_platki.jpg', thumbnail ='test/8in1_platki.jpg')
    
    def test_create_product(self):
        product = Product.objects.get(id=self.product.id)
        print(product.image.path)
        self.assertEqual(product.name, "test name")
        self.assertEqual(product.description, "test description")
        self.assertEqual(product.price, 2.00)
        self.assertEqual(product.category.name, "test category")

    def test_thumbnail_resized_correctly(self):
        # Tworzymy obraz o szerokości większej niż 200 pikseli
        image_path = os.path.join(os.getcwd(), 'media', 'products','thumbnail', '8in1_platki.jpg')
        image = Image.new('RGB', (300, 150))
        image.save(image_path)

        # Tworzymy produkt z przekraczającym szerokość obrazem
        product = Product.objects.create(
            name="test name",
            description="test description",
            price=2.00,
            category=self.category,
            thumbnail=image_path
        )
        product.save()

        resized_image = Image.open(product.thumbnail.path)
        self.assertEqual(resized_image.width, 200)

        
        expected_height = int(float(image.height) * (200 / float(image.width)))
        self.assertEqual(resized_image.height, expected_height)

        
        self.assertTrue(os.path.exists(product.thumbnail.path))

class OrderItemTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(name='Test Product', description='Description', price=10.00, category=category)
        self.order_item = OrderItem.objects.create(product=product, quantity=3)

    def test_order_item_str_method(self):
        self.assertEqual(str(self.order_item), 'Test Product - 3')

    def test_order_item_total_price(self):
        total_price = self.order_item.get_total_price()
        self.assertEqual(total_price, 30.00)


class OrderTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(name='Test Product', description='Description', price=10.00, category=category)
        order_item = OrderItem.objects.create(product=product, quantity=2)
        self.order = Order.objects.create(customer=user, shippingAddress='Test Address', paymentDue=None, ordered=True)
        self.order.orderItems.add(order_item)

    def test_order_total_price(self):
        total_price = self.order.get_total_price()
        self.assertEqual(total_price, 20.00)

    def test_order_items_count(self):
        items_count = self.order.orderItems.count()
        self.assertEqual(items_count, 1)

    def test_order_ordered_default_value(self):
        new_order = Order.objects.create(customer=self.order.customer, shippingAddress='New Address')
        self.assertFalse(new_order.ordered)