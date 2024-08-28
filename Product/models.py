
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1200)
    price = models.DecimalField(decimal_places=2, max_digits=7, default=00.00)
    image = models.FileField(upload_to='./media/', null=True)
    category = models.ForeignKey(to=Category ,on_delete=models.CASCADE, related_name='products', null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='products', null=True )
    
    def __str__(self):
        return self.title
    
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

