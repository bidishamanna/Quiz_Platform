from django.db import models
from account.models import User
from question_sets.models import Set
from category.models import Category
from subject.models import Subject
class Question(models.Model):
    OPTION_CHOICES = (      #..also can use list within tuple
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    delflag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text




from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.set.name} @ {self.started_at}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE,default=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, null=True, blank=True)

    is_correct = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)


# class UserAnswer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     selected_option = models.CharField(max_length=1)
#     correct_option = models.CharField(max_length=1)
#     attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
#     submitted_at = models.DateTimeField(auto_now_add=True)

