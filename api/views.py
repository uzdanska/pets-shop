from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import auth
from django.contrib import messages
from django.views.generic import View
from .forms import ProductForm, StatsForm
from django.core.paginator import Paginator
from .models import Product, Order, OrderItem, Category
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import  timedelta
from .tasks import send_payment_reminder_email
# Create your views here.

@login_required
def stats(request):
    if request.method == 'POST':
        form = StatsForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            num_result_products = form.cleaned_data['num_result_products']
            orders_in_date_range = Order.objects.filter(orderDate__range=(start_date, end_date))
            # orders_in_date_range = Order.objects.filter(orderDate__range=(start_date, end_date), ordered=True)

            product_quantity = {}
            for order in orders_in_date_range:
                order_items = order.orderItems.all()
                for order_item in order_items:
                    product_name = order_item.product.name
                    product_quantity[product_name] = order_item.quantity
            sorted_product_quantity = sorted(product_quantity.items(), key=lambda x: x[1], reverse=True)

            result_product = sorted_product_quantity[:num_result_products]
            return render(request, 'stats_result.html', {'result_product': result_product, 'start_date': start_date, 'end_date': end_date})
    else:
        form =StatsForm()

        return render(request, 'stats.html', {'form': form})


@login_required(login_url='login')
def order(request):
    user = request.user
    if user.is_authenticated:
        try:
            order = Order.objects.get(customer=request.user, ordered=False)
            order.paymentDue = timezone.now()
            dateOfPayment = order.paymentDue + timedelta(days=5)

            total_price = order.get_total_price()

            context = {
                'object': order, 
                'dateOfPayment': dateOfPayment,
                'total_price': total_price
            }

            if order.paymentDue == dateOfPayment -  timedelta(days=1) :
                eta = dateOfPayment - timezone.timedelta(days=1)
                send_payment_reminder_email.apply_async(args=[request.user.email], eta=eta)
            elif order.paymentDue == dateOfPayment:
                order.ordered = True
                order.save()

            # Send mail
            if settings.EMAIL_HOST_USER != "example@gmail.com":
                email = EmailMessage(
                    'Potwierdzenie zamówienia',
                    f"Dziękujemy za złożenie zamówienia {order.customer}. Kwota zamówienia wynosi {total_price}", 
                    settings.EMAIL_HOST_USER, 
                    [request.user.email]
                )
                email.fail_silently = False
                email.content_subtype = "html" 
                email.send()

            

            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                order_item.ordered = True
                order_item.save()

            return render(request, 'order.html', context)
        
        except Order.DoesNotExist:
            return redirect('/')

def product_list(request):
    queryset = Product.objects.all()
    name = request.GET.get('name', '')
    category = request.GET.get('category', '')
    description = request.GET.get('description', '')
    price = request.GET.get('price', '')
    sort_by = request.GET.get('sort')
    categories = Category.objects.all()

    if name:
        queryset = queryset.filter(name__icontains=name)
    if category:
        queryset = queryset.filter(category__name__icontains=category)
    if description:
        queryset = queryset.filter(description__icontains=description)
    if price:
        queryset = queryset.filter(price__icontains=price)

    if sort_by == 'name':
        queryset = queryset.order_by('name')
    elif sort_by == 'category':
        queryset = queryset.order_by('category__name')
    elif sort_by == 'price':
        queryset = queryset.order_by('price')

    paginator = Paginator(queryset, 4) 
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'name': name,
        'category': category,
        'description': description,
        'price': price,
        'categories': categories
    }

    return render(request, 'product_list.html', context)


def view_product(request, pk):
    if request.method == "GET":
        product = Product.objects.get(id=pk)

        return render(request, 'product.html', {'product': product})

@login_required(login_url='login')
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required(login_url='login')
def delete_product(request, pk):
    if request.method == "POST":
        product=Product.objects.get(id=pk)
        product.delete()
        return redirect('product-list')
    
@login_required(login_url='login')  
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print(product.image)

    if request.method =="GET":
        context = {'form': ProductForm(instance=product), 'id': pk}
        return render(request, 'edit_product.html', context)
    elif request.method=="POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if not request.FILES.get('image'):
                form.cleaned_data['image'] = product.image
            if not request.FILES.get('thumbnail'):
                form.cleaned_data['thumbnail'] = product.thumbnail
            form.save()
            messages.success(request, 'Produkt został zauktualizowany pomyslnie')
            return redirect('product', pk=pk)
        else:
            messages.error(request, "Prosze poprpawic bledy")
            # print(messages)
            return render(request, 'edit_product.html', {'form': form})


class OrderSummaryView(LoginRequiredMixin, View):
    # model = Order
    def get(self, *args, **kwargs):
        try:
            
            order = Order.objects.get(customer=self.request.user, ordered=False)
            # print(order)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Nie masz nic w koszyku. Dodaj produkt aby wyświetlić jego zawartość.")
            return redirect('/')
    
class RemoveOrderItemView(View):
    def post(self, request, order_item_id, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        if order_item.quantity > 1:
            order_item.quantity -= 1
            print(order_item)
            order_item.save()
        else:
            order_item.delete()
        return redirect('order_summary')
    
class AddQuantityOrderItem(View):
    def post(self, request, order_item_id, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        if order_item.quantity >= 1:
            order_item.quantity += 1
            print(order_item)
            print(order_item.quantity)
            order_item.save()
        
        return redirect('order_summary')
        

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_item, created = OrderItem.objects.get_or_create(product=product, ordered=False, quantity=1)    

    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderItems.filter(product__id=product.id).exists():
            # If the item already exists in the order, increment the quantity
            existing_order_item = order.orderItems.get(product__id=product.id)
            existing_order_item.quantity += 1
            existing_order_item.save()
            messages.info(request, "Ten produkt został ponownie dodany do twojego koszyka")
        else:
            # If the item is not in the order, add it to the order
            order.orderItems.add(order_item)
            messages.info(request, "Ten produkt został dodany do twojego koszyka")

        return redirect('/')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            customer=request.user, orderDate=ordered_date)
        order.orderItems.add(order_item)
        messages.info(request, "Ten produkt został dodany do twojego koszyka")
        return redirect('/')
 

def signin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')
    


# @api_view(['GET'])
# def getProducts(request):
#     product = Product.objects.all()
#     serializer = ProductSerializer(product, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getOrdersItem(request):
#     orderItem = OrderItem.objects.all()
#     serializer = OrderItemSerializer(orderItem, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getOrders(request):
#     order = Order.objects.all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)
