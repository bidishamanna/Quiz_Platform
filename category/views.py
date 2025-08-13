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
# # Create your views here.
# @login_required
# @role_required('staff')
# def recycle_bin(request):
#     deleted_categories = Category.objects.filter(delflag=True, user=request.user)
#     return render(request, "category/recycle_bin.html", {"deleted_categories": deleted_categories})
@login_required
@role_required('staff')
def recycle_bin(request):
    # 🔄 Show all deleted categories (not just ones owned by current user)
    deleted_categories = Category.objects.filter(delflag=True).select_related("user")

    return render(request, "category/recycle_bin.html", {
        "deleted_categories": deleted_categories,
        "user": request.user  # ✅ explicitly pass user for template checks
    })

@jwt_required
@role_required('staff')
@require_POST
def restore_category(request, pk):
    category = get_object_or_404(Category, pk=pk, delflag=True)

    if category.user != request.user:
        return JsonResponse({"message": "You do not have permission to restore this category."}, status=403)

    category.delflag = False
    category.save()

    return JsonResponse({"message": "Category restored successfully."})

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

        categories = Category.objects.filter(delflag=False)
        data = [{"id": c.id, "name": c.name} for c in categories]
        return JsonResponse({"message": "Category saved successfully!", "categories": data})

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

        if category.name.lower() == new_name.lower():
            return JsonResponse({"message": "No changes detected."}, status=200)

        # Check for existing active category with same name
        if Category.objects.filter(name__iexact=new_name, delflag=False).exclude(id=pk).exists():
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

