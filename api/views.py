from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import auth
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from .forms import ProductForm
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
from .models import Product, Order, OrderItem, Category
from django.contrib.auth.decorators import login_required
# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get('name')
        category = self.request.GET.get('category')
        description = self.request.GET.get('description')
        price = self.request.GET.get('price')
        sort_by = self.request.GET.get('sort')

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

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        context['category'] = self.request.GET.get('category', '')
        context['description'] = self.request.GET.get('description', '')
        context['price'] = self.request.GET.get('price', '')
        context['products'] = self.get_queryset()

        return context

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
    product = get_object_or_404(Product, id=pk)

    form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'pk': pk})

class OrderSummaryView(View):
    # model = Order
    def get(self, *args, **kwargs):
        return render(self.request, "order_summary.html")
    # template = "order_summary.html"

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
    



# class EditProductView(UpdateView):
#     model = Product
#     template_name= 'edit_product.html'
#     fields = ['name', 'descrption', 'name', 'descrption', 'price', 'category', 'image', 'thumbnail']

    

# def product_list(request):
#     # Filtrowanie
#     category = request.GET.get('category')
#     if category:
#         products = Product.objects.filter(category=category)
#     else:
#         products = Product.objects.all()
    
#     # Sortowanie
#     sort_by = request.GET.get('sort_by', 'name')  
#     products = products.order_by(sort_by)
    
#     # Paginacja
#     paginator = Paginator(products, 10)  # Pokazuj 10 produktów na stronę
#     page = request.GET.get('page')
#     products = paginator.get_page(page)
    
#     return render(request, 'product_list.html', {'products': products})

@api_view(['GET'])
def getProducts(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOrdersItem(request):
    orderItem = OrderItem.objects.all()
    serializer = OrderItemSerializer(orderItem, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOrders(request):
    order = Order.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)
