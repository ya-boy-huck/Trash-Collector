from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
 
    def __str__(self):
        return self.name

# TODO: Create an Employee model with properties required by the user stories