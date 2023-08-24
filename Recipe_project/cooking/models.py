from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipe(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    r_name=models.CharField(max_length=100)
    r_description=models.TextField(blank=True)
    r_image=models.ImageField(upload_to='recipe_image')
    r_view_count=models.IntegerField(default=1)