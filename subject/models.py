from django.db import models

# Create your models here.
from django.db import models
from category.models import Category
from account.models import User 
# class Subject(models.Model):
#     name = models.CharField(max_length=100,help_text="Name of the subject (e.g., Mathematics, Physics)")
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subjects", help_text="Category associated with this subject")
#     delflag = models.BooleanField(default=False) 
#     # unique_together inside Meta is a Django-specific keyword
#     user = models.ForeignKey(User, on_delete=models.CASCADE) 
#     requires_payment = models.BooleanField(
#         default=False,
#         help_text="If true, user must pay to access tests under this subject"
#     )

#     price = models.DecimalField(
#         max_digits=7,
#         decimal_places=2,
#         default=0.00,
#         help_text="Enter price for accessing the test. Used only if requires_payment=True"
#     )
#     class Meta:
#         unique_together = ('name', 'category') 

#     def __str__(self):
#         return f"{self.name} - {self.category.name}"


from django.utils.text import slugify

class Subject(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the subject (e.g., Mathematics, Physics)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subjects", help_text="Category associated with this subject")
    delflag = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE
                             )
    requires_payment = models.BooleanField(
        default=False,
        help_text="If true, user must pay to access tests under this subject"
    )
    
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        help_text="Enter price for accessing the test. Used only if requires_payment=True"
    )
    
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="Auto-generated from subject name")

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Subject.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



