from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from category.models import Category
from subject.models import Subject
from django.shortcuts import render
from category.models import Category
from subject.models import Subject

# def home(request):
#     # Get all active categories
#     categories = Category.objects.filter(delflag=False)

#     # Prepare a dictionary that maps each category to its subjects
#     category_subject_map = {}
#     for category in categories:
#         subjects = Subject.objects.filter(category=category, delflag=False)
#         category_subject_map[category] = subjects

#     # Pass the map to the template
#     return render(request, 'about/home.html', {
#         'category_subject_map': category_subject_map
#     })

# views.py
from django.shortcuts import render
from subject.models import Category
from payment.models import Payment

def home(request):
    categories = Category.objects.filter(delflag=False)
    category_subject_map = {}

    paid_subjects = set() 
    if request.user.is_authenticated:
        paid_subjects = set(
            Payment.objects.filter(
                user=request.user,
                status='SUCCESS'
            ).values_list('subject_id', flat=True) # value_list -- Instead of fetching full model objects, just return a list (or tuple) of specific field values.”
        )                                        # it looks like this [(2,), (5,), (7,)],, then flat = True ,, it “flattens” that into a simple list:[2, 5, 7]
 


    for category in categories:
        subjects = category.subjects.filter(delflag=False)  #related_name="subjects", Django automatically creates an attribute .subjects on each Category object.
                                                         #category.subjects = all subjects that belong to that category.
        category_subject_map[category] = subjects     

    return render(request, 'about/home.html', {
        'category_subject_map': category_subject_map,
        'paid_subjects': paid_subjects,
    })

# from django.contrib.auth.decorators import login_required
# from .models import Category, Subject
# from payment.models import Payment

# @login_required
# def home(request):
#     # Get all active categories
#     categories = Category.objects.filter(delflag=False)

#     # Prepare category-subject mapping
#     category_subject_map = {}
#     for category in categories:
#         subjects = Subject.objects.filter(category=category, delflag=False)
#         category_subject_map[category] = subjects

#     # Get paid subject IDs for this user
#     paid_subject_ids = Payment.objects.filter(
#         user=request.user,
#         status='success'
#     ).values_list('subject_id', flat=True)

#     return render(request, 'about/home.html', {
#         'category_subject_map': category_subject_map,
#         'paid_subject_ids': list(paid_subject_ids),  # convert to list for template
#     })


def contact(request):
    return render(request,'about/contact.html')

def about(request):
    return render(request,'about/about.html')

