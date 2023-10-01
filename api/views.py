from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from .forms import ProductForm
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
from .models import Product, Order, OrderItem
# Create your views here.

class ProductListView(ListView):
    model = Product
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10 

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get('name')
        category = self.request.GET.get('category')
        description = self.request.GET.get('description')
        price = self.request.GET.get('price')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if price:
            queryset = queryset.filter(price__icontains=price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        context['category'] = self.request.GET.get('category', '')
        context['description'] = self.request.GET.get('description', '')
        context['price'] = self.request.GET.get('price', '')


        return context

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')  # Przekieruj użytkownika do listy produktów po dodaniu produktu
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def delete_product(request, pk):
    if request.method == "POST":
        product=Product.objects.get(id=pk)
        product.delete()
        return redirect('product-list')
    
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

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
