from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import role_required
# Create your views here.
from .models import Set
from category.models import Category
from subject.models import Subject
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from account.decorators import jwt_required
from account.decorators import role_required
from django.views.decorators.http import require_POST

@login_required
@role_required('staff')
def set_recycle_bin(request):
    deleted_sets = Set.objects.select_related("category", "subject", "user").filter(delflag=True)
    return render(request, "question_sets/recycle_bin.html", {
        "deleted_sets": deleted_sets,
        "user": request.user
    })


@jwt_required
@role_required('staff')
@require_POST
def restore_set(request, pk):
    s = get_object_or_404(Set, pk=pk, delflag=True)

    if s.user != request.user:
        return JsonResponse({"message": "You do not have permission to restore this set."}, status=403)

    s.delflag = False
    s.save()
    return JsonResponse({"message": "Set restored successfully."})

@login_required
@role_required('staff')  # Only staff allowed
def set_list(request):
    user = request.user
    categories = Category.objects.filter(delflag=False)
    subjects = Subject.objects.filter(delflag=False)
    sets = Set.objects.select_related("category", "subject", "user").filter(delflag=False).order_by("id")

    return render(request, "question_sets/set_list.html", {
        "sets": sets,
        "categories": categories,
        "subjects": subjects,
        "user_role": user.role,
    })

@jwt_required
@role_required('staff')
def get_subjects(request):
    category_id = request.GET.get("category_id")

    if not category_id:
        return JsonResponse({"message": "Category ID is required."}, status=400)

    try:
        Category.objects.get(id=category_id, delflag=False)
        subjects = Subject.objects.filter(category_id=category_id, delflag=False).values("id", "name")
        return JsonResponse({"subjects": list(subjects)})
    except Category.DoesNotExist:
        return JsonResponse({"message": "Invalid category ID."}, status=400)
    
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

@jwt_required
@role_required('staff')
@require_http_methods(["GET", "POST"])
def add_set(request):
    if request.method == "GET":
        categories = Category.objects.filter(delflag=False)
        subjects = Subject.objects.filter(delflag=False)
        sets = Set.objects.select_related("category", "subject", "user").filter(delflag=False)
        return render(request, "question_sets/add_set.html", {
            "categories": categories,
            "subjects": subjects,
            "sets": sets,
            "user_role": request.user.role,
        })

    # POST request — Add set logic
    set_name = request.POST.get("set_name")
    category_id = request.POST.get("category")
    subject_id = request.POST.get("subject")

    if set_name and category_id and subject_id:
        try:
            category = Category.objects.get(id=category_id, delflag=False)
            subject = Subject.objects.get(id=subject_id, category=category, delflag=False)

            # Reactivate if previously soft-deleted
            soft_deleted = Set.objects.filter(
                name=set_name,
                category=category,
                subject=subject,
                delflag=True
            ).first()

            if soft_deleted:
                soft_deleted.delflag = False
                soft_deleted.user = request.user
                soft_deleted.save()
            else:
                # Prevent duplicates based on unique_together constraint
                if Set.objects.filter(
                    name=set_name,
                    category=category,
                    subject=subject,
                    delflag=False
                ).exists():
                    return JsonResponse({"message": "Set already exists for this subject and category."}, status=400)

                Set.objects.create(
                    name=set_name,
                    category=category,
                    subject=subject,
                    user=request.user
                )

            # Fetch and render updated set rows
            sets = Set.objects.select_related("category", "subject", "user").filter(delflag=False)
            html = render_to_string("partials/set_rows.html", {
                "sets": sets,
                "user_role": request.user.role,
                "user": request.user,  # 🔥 Add this line!
            })


            return JsonResponse({"message": "Set added successfully!", "html": html})

        except (Category.DoesNotExist, Subject.DoesNotExist):
            return JsonResponse({"message": "Invalid category or subject selected."}, status=400)

    return JsonResponse({"message": "All fields are required (Set name, Category, Subject)."}, status=400)

from django.contrib.auth.decorators import login_required
from account.decorators import role_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Set

@login_required
@role_required('staff')
def get_set_rows(request):
    sets = Set.objects.select_related("category", "subject", "user").filter(delflag=False).order_by("id")
    html = render_to_string("partials/set_rows.html", {
    "sets": sets,
    "user_role": request.user.role,
    "user": request.user,  
    })

    return JsonResponse({"html": html})

from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from subject.models import Subject
from category.models import Category

@jwt_required
@role_required('staff')
@require_POST
def edit_set(request, pk):
    set_obj = get_object_or_404(Set, pk=pk, delflag=False)

    if set_obj.user != request.user:
        return JsonResponse({"message": "Unauthorized. You can only edit your own set."}, status=403)

    set_name = request.POST.get("set_name")
    category_id = request.POST.get("category")
    subject_id = request.POST.get("subject")

    if set_name and category_id and subject_id:
        try:
            category = Category.objects.get(id=category_id, delflag=False)
            subject = Subject.objects.get(id=subject_id, category=category, delflag=False)

            # Check for duplicate
            if Set.objects.filter(
                name=set_name, category=category, subject=subject, delflag=False
            ).exclude(id=set_obj.id).exists():
                return JsonResponse({"message": "Set with this name already exists for the selected subject."}, status=400)

            # Update
            set_obj.name = set_name
            set_obj.category = category
            set_obj.subject = subject
            set_obj.save()

            sets = Set.objects.select_related("category", "subject", "user").filter(delflag=False)
            html = render_to_string("partials/set_rows.html", {
                "sets": sets,
                "user_role": request.user.role,
            }, request=request)

            return JsonResponse({"message": "Set updated successfully!", "html": html})

        except (Category.DoesNotExist, Subject.DoesNotExist):
            return JsonResponse({"message": "Invalid category or subject."}, status=400)

    return JsonResponse({"message": "All fields are required."}, status=400)


@jwt_required
@role_required('staff')
@require_POST
def delete_set(request, pk):
    set_obj = get_object_or_404(Set, pk=pk, delflag=False)

    if set_obj.user != request.user:
        return JsonResponse({"message": "Unauthorized. You can only delete your own set."}, status=403)

    set_obj.delflag = True
    set_obj.save()

    return JsonResponse({
        "message": "Set deleted successfully."
    })

# from django.template.loader import render_to_string

# @jwt_required
# @role_required('staff')
# @require_POST
# def delete_set(request, pk):
#     set_obj = get_object_or_404(Set, pk=pk, delflag=False)

#     if set_obj.user != request.user:
#         return JsonResponse({"message": "Unauthorized. You can only delete your own set."}, status=403)

#     set_obj.delflag = True
#     set_obj.save()

#     # Get updated list
#     sets = Set.objects.select_related("category", "subject", "user").filter(delflag=False)
#     html = render_to_string("partials/set_rows.html", {"sets": sets, "user_role": "staff", "user": request.user})

#     return JsonResponse({
#         "message": "Set deleted successfully.",
#         "html": html
#     })

