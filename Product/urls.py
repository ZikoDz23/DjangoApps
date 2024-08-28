from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.blank),
    path('home/',views.home,name='home'),
    path('register/',views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login') , name='logout'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('add_product/', views.addproduct, name='add_product'),
    path('product/<str:product_title>/', views.productpage, name='product_details'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    path('profile/<str:username>/update/', views.update_profile, name='update_profile'),
    path('product/<str:username>/delete/<int:product_id>/', views.delete_product, name='delete_product'),

]
