from django.shortcuts import render,redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProductForm

# Create your views here.
def blank(request):
    return redirect('home')
    
def home(request):
    laptops = Product.objects.filter(category=2)
    smartphones = Product.objects.filter(category=1)
    profile = Profile.objects.get(user=request.user)
    context = {'laptops':laptops,
               'smartphones':smartphones,
               'profile':profile
               }
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
    profile = Profile.objects.get(user=request.user)
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
        'profile':profile
    }
    return render(request, 'category.html', context)
    
@login_required
def addproduct(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Use request.FILES for file uploads
        category_name = request.POST.get('cat')  
        user = request.user  # Assuming the user is logged in

        if title and category_name and user:
            try:
                category = Category.objects.get(name=category_name)
                new_product = Product(
                    title=title,
                    description=description,
                    price=price,
                    image=image,
                    category=category,
                    user=user
                )
                new_product.save()
                messages.success(request, 'Product added successfully.')
                return redirect(f'/profile/{user.username}/')  # Redirect after saving
            except Category.DoesNotExist:
                messages.error(request, 'Category does not exist.')
    else:
        messages.error(request, 'Form submission failed.')

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})


def productpage(request, product_title):
    product = get_object_or_404(Product, title=product_title)
    profile = Profile.objects.get(user=request.user)
    context ={
        'product':product,
        'profile':profile
    }
    return render(request, 'product.html', context)

def public_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    products = Product.objects.filter(user=profile.user)
    context = {
        'profile': profile,
        'products': products
    }
    return render(request, 'public_profile.html', context)
    
from django.urls import reverse

@login_required
def update_profile(request, username):
    # Get the user based on the provided username
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to the updated profile page
            return redirect('public_profile', username=username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form, 'username': username})



@login_required
def delete_product(request, product_id, username):
    user = get_object_or_404(User, username=username)
    product = get_object_or_404(Product, id=product_id, user=user)
    if request.method == 'POST':
        product.delete()
        return redirect('profile')
    return render(request, 'confirm_delete.html', {'product': product})