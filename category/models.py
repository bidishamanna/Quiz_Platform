from django.db import models

# Create your models here.
from account.models import User
class Category(models.Model):   # models — it's a module. # Model -- is a class inside the models module.

    name = models.CharField(max_length=100, unique=True, help_text="Name of the Category (e.g., Python, Java,)")
    delflag = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    def __str__(self):

        return self.name


