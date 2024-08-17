from django.shortcuts import render,redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    laptops = Product.objects.filter(category=2)
    smartphones = Product.objects.filter(category=1)
    context = {'laptops':laptops,
               'smartphones':smartphones}
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        if username :
            new_user = User(username=username, email=email, password=password)
            new_user.save()
        
    return render(request, 'register.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home URL pattern
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    product_count = products.count() 
    sort_option = request.GET.get('sort', 'name')
    
    # Sort the products based on the selected option
    if sort_option == 'price_asc':
        products = Product.objects.filter(category=category).order_by('price')
    elif sort_option == 'price_desc':
        products = Product.objects.filter(category=category).order_by('-price')

    context ={
        'category': category,
        'products': products,
        'product_count': product_count,
        'sort_option': sort_option,
    }
    return render(request, 'category.html', context)
    
    
def addproduct(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.POST.get('image')     
        if title:
            new_product = Product(title=title, description=description, price=price, image=image)
            new_product.save()
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'add_product.html', context)

def productpage(request, product_title):
    product = get_object_or_404(Product, title=product_title)
    context ={
        'product':product
    }
    return render(request, 'product.html', context)