from django.db import models

# Create your models here.
from account.models import User
from subject.models import Subject
from category.models import Category


class Set(models.Model): # models — it's a module. # Model -- is a class inside the models module.

    name = models.CharField(max_length=100)  # No unique=True
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delflag = models.BooleanField(default=False)  # Active by default
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "category", "subject")  # Prevents duplicate sets under same subject & category

    def __str__(self):
        return self.name


