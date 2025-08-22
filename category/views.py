from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from account.decorators import role_required,jwt_required
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from subject.models import Subject
from question_sets.models import Set
from questions.models import Question
# # Create your views here.
import re
@login_required
@role_required('staff')
def recycle_bin(request):
    # 🔄 Show all deleted categories (not just ones owned by current user)
    deleted_categories = Category.objects.filter(delflag=True).select_related("user") 

    return render(request, "category/recycle_bin.html", {
        "deleted_categories": deleted_categories,
        "user": request.user  # ✅ explicitly pass user for template checks
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

# //////// if i want who create the category , after anyone restore but ownership will be go who create this caregory //////////////
# @jwt_required
# @role_required('staff')  # Ensures only staff can restore categories
# @require_POST
# def restore_category(request, pk):
#     # Fetch the category which is soft-deleted
#     category = get_object_or_404(Category, pk=pk, delflag=True)

#     # If the user is staff, restore the category
#     category.delflag = False
#     category.save()

#     return JsonResponse({"message": "Category restored successfully."})



# ///////////  who restore the category ownership will assign to that staff///////

@jwt_required
@role_required('staff')  # Ensures only staff can restore categories
@require_POST
def restore_category(request, pk):
    # Fetch the category which is soft-deleted
    category = get_object_or_404(Category, pk=pk, delflag=True)

    # Restore and transfer ownership to the user performing the action
    category.delflag = False
    category.user = request.user
    category.save()
    # ✅ Restore all related subjects
      # ✅ Restore all related subjects under this category
    Subject.objects.filter(category=category, delflag=True).update(
        delflag=False,
        user=request.user
    )

    # ✅ Restore all related sets under those subjects
    Set.objects.filter(subject__category=category, delflag=True).update(
        delflag=False,
        user=request.user
    )

    # ✅ Restore all related questions under those sets
    Question.objects.filter(set__subject__category=category, delflag=True).update(
        delflag=False,
        user=request.user
    )


    return JsonResponse({
        "message": "Category restored successfully "
    })


@login_required
@role_required('staff', 'student')
def category_list(request):
    categories = Category.objects.filter(delflag=False)
    return render(request, "category/category_list.html", {"categories": categories})



@login_required
@role_required('staff')
def get_category_rows(request):
    categories = Category.objects.filter(delflag=False)
    html = render_to_string('partials/category_rows.html', {
        "categories": categories,
        "user": request.user  # ✅ Pass user here
    })
    return JsonResponse({"html": html})


@jwt_required 
@role_required('staff')
@require_http_methods(["GET", "POST"])
def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("category_name", "").strip()

        if not category_name:
            return JsonResponse({"message": "Category name cannot be empty!"}, status=400)
        
         # ✅ Regex check: only uppercase letters allowed (A–Z), at least 1 char
        if not re.fullmatch(r"[A-Z]+", category_name):
            return JsonResponse(
                {"message": "Category name must contain only capital letters (A–Z)."}, 
                status=400
            )
        # Case-insensitive check among active categories
        if Category.objects.filter(name__iexact=category_name, delflag=False).exists():
            return JsonResponse({"message": "Category with this name already exists."}, status=400)

        # If soft-deleted version exists, restore it
        deleted = Category.objects.filter(name__iexact=category_name, delflag=True).first()
        if deleted:
            deleted.name = category_name
            deleted.delflag = False
            deleted.user = request.user  # optionally update the owner
            deleted.save()
            messages.success(request, "Category reactivated successfully!")
        else:
            Category.objects.create(name=category_name, user=request.user)
            messages.success(request, "Category created successfully!")

        # categories = Category.objects.filter(delflag=False)
        # data = [{"id": c.id, "name": c.name} for c in categories] #category instantly appear in table"
        # return JsonResponse({"message": "Category saved successfully!", "categories": data})

    # GET request: render the form and category list
    categories = Category.objects.filter(delflag=False)
    return render(request, "category/add_category.html", {"categories": categories})


@jwt_required
@role_required('staff')

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if category.user != request.user:
        return JsonResponse({"message": "You do not have permission to edit this category."}, status=403)

    if request.method == "POST":
        new_name = request.POST.get("category_name", "").strip()

        if not new_name:
            return JsonResponse({"message": "Category name cannot be empty!"}, status=400)
        
        if not re.fullmatch(r"[A-Z]+", new_name):
            return JsonResponse(
                {"message": "Category name must contain only capital letters (A–Z)."},
                status=400
            )
        if category.name.lower() == new_name.lower():
            return JsonResponse({"message": "No changes detected."}, status=200)

        # Check for existing active category with same name 

        if Category.objects.filter(name__iexact=new_name, delflag=False).exclude(id=pk).exists():  # skip its own id and search all except own id
            return JsonResponse({"message": "Another active category with this name already exists."}, status=400)

        # Reactivate a previously deleted category
        deleted = Category.objects.filter(name__iexact=new_name, delflag=True).first() 
        if deleted:
            deleted.delflag = False
            deleted.user = request.user  # reassign ownership
            deleted.save()

            category.delflag = True
            category.save()

            # ✅ Set correct ownership
            updated_category = deleted
        else:
            category.name = new_name
            category.save()
            updated_category = category

        # ✅ Ensure only categories belonging to the user show buttons
        categories = Category.objects.filter(delflag=False)
        html = render_to_string("partials/category_rows.html", {
            "categories": categories,
            "user": request.user
        })

        return JsonResponse({
            "message": "Category updated successfully.",
            "html": html
        })


@jwt_required 
@role_required('staff')
@require_POST 
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # ✅ Only allow deletion by the creator of the category
    if category.user != request.user:
        return JsonResponse({"message": "You do not have permission to delete this category."}, status=403)

    category.delflag = True
    category.save()
    # ✅ Soft delete all related subjects
        # ✅ Soft delete all subjects under the category
    Subject.objects.filter(category=category, delflag=False).update(delflag=True)

    # ✅ Soft delete all sets under those subjects
    Set.objects.filter(subject__category=category, delflag=False).update(delflag=True)

    # ✅ Soft delete all questions under those sets
    Question.objects.filter(set__subject__category=category, delflag=False).update(delflag=True) #lookups across relationships

    # 🔁 Return updated category rows with current user context
    categories = Category.objects.filter(delflag=False)
    html = render_to_string("partials/category_rows.html", {
        "categories": categories,
        "user": request.user  # 🧠 Needed to determine Edit/Delete buttons
    })

    return JsonResponse({
        "message": "Category deleted successfully.",
        "html": html
    })

