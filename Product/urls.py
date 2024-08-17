from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/',views.home,name='home'),
    path('register/',views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login') , name='logout'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('add_product/', views.addproduct),
    path('product/<str:product_title>/', views.productpage, name='product_details'),
    
    
]
