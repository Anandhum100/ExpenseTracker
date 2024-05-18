
from django.db import models
from django.contrib.auth.models import User

# Create your models here.





class AddExpensedb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    NAME = models.CharField(max_length=50, null=True, blank=True)
    ExpenseName = models.CharField(max_length=50, null=True, blank=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Date = models.DateField(blank=True, null=True)
    ExpenseCategory = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.NAME


class ProfileUpdate(models.Model):
    FullName = models.CharField(max_length=50, null=True, blank=True)
    PHONE = models.IntegerField( null=True, blank=True)
    StreetAddress = models.CharField(max_length=50, null=True, blank=True)
    COUNTRY =  models.CharField(max_length=50, null=True, blank=True)
    ZipCode =   models.IntegerField( null=True, blank=True)
    UserImage =  models.ImageField(upload_to="Media/Userimage",null=True,blank=True)
    
    
    
    
    
    