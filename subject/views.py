

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from account.decorators import jwt_required, role_required
from .models import Subject
from category.models import Category
from django.contrib.auth.decorators import login_required

@login_required
@role_required('staff')
def subject_recycle_bin(request):
    # ✅ Show all deleted subjects created by any staff
    deleted_subjects = Subject.objects.select_related("category", "user").filter(delflag=True)

    return render(request, "subject/recycle_bin.html", {
        "deleted_subjects": deleted_subjects,
        "user": request.user  # ✅ Needed for template checks (ownership)
    })

@jwt_required
@role_required('staff')
@require_POST
def restore_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, delflag=True)

    if subject.user != request.user:
        return JsonResponse({"message": "You do not have permission to restore this subject."}, status=403)

    subject.delflag = False
    subject.save()

    return JsonResponse({"message": "Subject restored successfully."})


@login_required
@role_required('staff', 'student')
def subject_list(request):
    user = request.user
    categories = Category.objects.filter(delflag=False)
    subjects = Subject.objects.select_related("category").filter(delflag=False).order_by("id")

    return render(request, "subject/subject_list.html", {
        "categories": categories,
        "subjects": subjects,
        "user_role": user.role,  # Add role to context
    })


from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Subject


#     if request.method == "GET":
#         categories = Category.objects.filter(delflag=False)
#         subjects = Subject.objects.select_related("category").filter(delflag=False)
#         return render(request, "subject/add_subject.html", {
#             "categories": categories,
#             "subjects": subjects,
#             "user_role": request.user.role,
#         })

#     # POST request — Add subject logic
#     category_id = request.POST.get("category")
#     subject_name = request.POST.get("subject_name")
#     requires_payment = request.POST.get("requires_payment") == "on"
#     price = request.POST.get("price") or 0.00

#     if subject_name and category_id:
#         try:
#             category = Category.objects.get(id=category_id, delflag=False)

#             soft_deleted = Subject.objects.filter(name=subject_name, category=category, delflag=True).first()
#             if soft_deleted:
#                 soft_deleted.delflag = False
#                 soft_deleted.user = request.user
#                 soft_deleted.requires_payment = requires_payment
#                 soft_deleted.price = price if requires_payment else 0.00
#                 soft_deleted.save()
#             else:
#                 if Subject.objects.filter(name=subject_name, category=category, delflag=False).exists():
#                     return JsonResponse({"message": "Subject already exists for this department."}, status=400)

#                 Subject.objects.create(
#                     name=subject_name,
#                     category=category,
#                     user=request.user,
#                     requires_payment=requires_payment,
#                     price=price if requires_payment else 0.00
#                 )

#             subjects = Subject.objects.select_related("category").filter(delflag=False)
#             html = render_to_string("partials/subject_rows.html", {
#                 "subjects": subjects,
#                 "user_role": request.user.role,
                
#             })

#             return JsonResponse({"message": "Subject added successfully!", "html": html})

#         except Category.DoesNotExist:
#             return JsonResponse({"message": "Selected category does not exist or is deleted."}, status=400)

#     return JsonResponse({"message": "All fields are required."}, status=400)
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
# from django.template.loader import render_to_string
# from your_app.models import Category, Subject  # adjust as needed
# from your_app.decorators import jwt_required, role_required  # adjust as needed


# @jwt_required
# @role_required('staff')
# @require_http_methods(["GET", "POST"])
# def add_subject(request):
#     if request.method == "GET":
#         categories = Category.objects.filter(delflag=False)
#         subjects = Subject.objects.select_related("category").filter(delflag=False)
#         return render(request, "subject/add_subject.html", {
#             "categories": categories,
#             "subjects": subjects,
#             "user_role": request.user.role,
#         })

#     # POST request — Add subject logic
#     category_id = request.POST.get("category")
#     subject_name = request.POST.get("subject_name")
#     requires_payment = request.POST.get("requires_payment") == "on"

#     # 🔒 Safely convert price using Decimal
#     raw_price = request.POST.get("price")
#     try:
#         price = Decimal(raw_price) if raw_price else Decimal("0.00")
#     except InvalidOperation:
#         return JsonResponse({"message": "Invalid price value."}, status=400)

#     if subject_name and category_id:
#         try:
#             category = Category.objects.get(id=category_id, delflag=False)

#             soft_deleted = Subject.objects.filter(name=subject_name, category=category, delflag=True).first()
#             if soft_deleted:
#                 soft_deleted.delflag = False
#                 soft_deleted.user = request.user
#                 soft_deleted.requires_payment = requires_payment
#                 soft_deleted.price = price if requires_payment else Decimal("0.00")
#                 soft_deleted.save()
#             else:
#                 if Subject.objects.filter(name=subject_name, category=category, delflag=False).exists():
#                     return JsonResponse({"message": "Subject already exists for this department."}, status=400)

#                 Subject.objects.create(
#                     name=subject_name,
#                     category=category,
#                     user=request.user,
#                     requires_payment=requires_payment,
#                     price=price if requires_payment else Decimal("0.00")
#                 )

#             subjects = Subject.objects.select_related("category").filter(delflag=False)
#             html = render_to_string("partials/subject_rows.html", {
#                 "subjects": subjects,
#                 "user_role": request.user.role,
#             })

#             return JsonResponse({"message": "Subject added successfully!", "html": html})

#         except Category.DoesNotExist:
#             return JsonResponse({"message": "Selected category does not exist or is deleted."}, status=400)

#     return JsonResponse({"message": "All fields are required."}, status=400)

from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .models import Subject, Category
# from .decorators import jwt_required, role_required

@jwt_required
@role_required('staff')
@require_http_methods(["GET", "POST"])
def add_subject(request):
    if request.method == "GET":
        categories = Category.objects.filter(delflag=False)   # need for template dropdown
        subjects = Subject.objects.select_related("category").filter(delflag=False)   #table rendering
        return render(request, "subject/add_subject.html", {
            "categories": categories,
            "subjects": subjects,
            "user_role": request.user.role,
        })

    # POST logic
    category_id = request.POST.get("category")
    subject_name = request.POST.get("subject_name")
    requires_payment = request.POST.get("requires_payment") == "true" 


    raw_price = request.POST.get("price")
    try:
        price = Decimal(raw_price) if raw_price else Decimal("0.00")
    except InvalidOperation:
        return JsonResponse({"message": "Invalid price value."}, status=400)

    # If not paid, price should always be 0.00
    if not requires_payment:
        price = Decimal("0.00")

    if subject_name and category_id:
        try:
            category = Category.objects.get(id=category_id, delflag=False)

            # Check for soft-deleted subject
            soft_deleted = Subject.objects.filter(name=subject_name, category=category, delflag=True).first()
            if soft_deleted:
                soft_deleted.delflag = False
                soft_deleted.user = request.user
                soft_deleted.requires_payment = requires_payment
                soft_deleted.price = price
                soft_deleted.save()
            else:
                if Subject.objects.filter(name=subject_name, category=category, delflag=False).exists():
                    return JsonResponse({"message": "Subject already exists for this department."}, status=400)

                Subject.objects.create(
                    name=subject_name,
                    category=category,
                    user=request.user,
                    requires_payment=requires_payment,
                    price=price
                )

            # Re-fetch subjects for rendering
            subjects = Subject.objects.select_related("category").filter(delflag=False)
            html = render_to_string("partials/subject_rows.html", {
                "subjects": subjects,
                "user_role": request.user.role,
                "user": request.user,  # Make sure 'user' is passed!
            })

            return JsonResponse({"message": "Subject added successfully!", "html": html})

        except Category.DoesNotExist:
            return JsonResponse({"message": "Selected category does not exist or is deleted."}, status=400)

    return JsonResponse({"message": "All fields are required."}, status=400)

@login_required
@role_required('staff')
def get_subject_rows(request):
    subjects = Subject.objects.select_related("category").filter(delflag=False).order_by("id")
    html = render_to_string(
        "partials/subject_rows.html",
        {
            "subjects": subjects,
            "user_role": request.user.role,
            "user": request.user,  # ✅ Add this line!
        },
        request=request
    )
    return JsonResponse({"html": html})

from django.template.loader import render_to_string


@jwt_required
@role_required('staff')
@require_POST
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, delflag=False)

    if subject.user != request.user:
        return JsonResponse({"message": "Unauthorized. You can only edit your own subject."}, status=403)

    subject_name = request.POST.get("subject_name")
    category_id = request.POST.get("category")
    requires_payment = request.POST.get("requires_payment") == "true"

    raw_price = request.POST.get("price")
    try:
        price = Decimal(raw_price) if raw_price else Decimal("0.00")
    except InvalidOperation:
        return JsonResponse({"message": "Invalid price value."}, status=400)

    if not requires_payment:
        price = Decimal("0.00")

    if subject_name and category_id:
        try:
            category = Category.objects.get(id=category_id, delflag=False)

            # Check for duplicates excluding current subject
            if Subject.objects.filter(
                name=subject_name, category=category, delflag=False
            ).exclude(id=subject.id).exists():
                return JsonResponse({"message": "Subject with this name already exists in the selected category."}, status=400)

            subject.name = subject_name
            subject.category = category
            subject.requires_payment = requires_payment
            subject.price = price
            subject.save()

            subjects = Subject.objects.select_related("category").filter(delflag=False)
            html = render_to_string(
                "partials/subject_rows.html",
                {
                    "subjects": subjects,
                    "user_role": request.user.role,
                    "user": request.user,
                },
                request=request
            )

            return JsonResponse({"message": "Subject updated successfully!", "html": html})

        except Category.DoesNotExist:
            return JsonResponse({"message": "Selected category not found."}, status=400)

    return JsonResponse({"message": "All fields are required."}, status=400)

@jwt_required
@role_required('staff')
@require_POST
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, delflag=False)
    if subject.user != request.user:
        return JsonResponse({"message": "Unauthorized. You can only delete your own subject."}, status=403)

    subject.delflag = True
    subject.save()

    subjects = Subject.objects.select_related("category").filter(delflag=False)
    subject_data = [
        {
            "id": s.id,
            "name": s.name,
            "category_id": s.category.id,
            "category_name": s.category.name,
        }
        for s in subjects
    ]
    return JsonResponse({
        "message": "Subject deleted successfully.",
        "subjects": subject_data
    })

# @jwt_required
# @role_required('student')
# def view_subjects(request):
#     subjects = Subject.objects.select_related("category").filter(delflag=False).order_by("id")
#     return render(request, "subject/student_subject_list.html", {
#         "subjects": subjects
#     })
# this view is full fill my Action	Allowed?	Condition
# Staff A creates category "ML"	✅	Only Staff A can edit/delete it
# Staff B adds "Data Science" subject under "ML"	✅	Any staff can add under other's category
# Staff A tries to delete subject created by Staff B	❌	Only creator of subject can do this............and student only see category and under that category which subjects are their


