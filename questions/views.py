from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Category,Set,Question
from django.contrib import messages 
import random
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Question
from category.models import Category
from subject.models import Subject
from question_sets.models import Set
from django.template.loader import render_to_string
from account.decorators import jwt_required
from account.decorators import role_required
from django.views.decorators.http import require_POST
import csv
import io
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from category.models import Category
from subject.models import Subject
from question_sets.models import Set
from quiz.models import Question
import pandas as pd

# @jwt_required
# @role_required('staff')
# @require_http_methods(["GET", "POST"])
# def upload_questions(request):
#     if request.method == "GET":
#         categories = Category.objects.filter(delflag=False)
#         subjects = Subject.objects.filter(delflag=False)
#         sets = Set.objects.filter(user=request.user, delflag=False)  # Only sets created by this staff

#         # ✅ Load existing questions created by this staff
#         questions = Question.objects.select_related("category", "subject", "set", "user").filter(
#             user=request.user,
#             delflag=False
#         ).order_by('id')

#         return render(request, "questions/csv_question_file_upload.html", {
#             "categories": categories,
#             "subjects": subjects,
#             "sets": sets,
#             "questions": questions,  # Pass to template for table rendering
#             "user_role": request.user.role,
#             "user": request.user,
#         })

#     # POST request — Handle file upload
#     uploaded_file = request.FILES.get("file")
#     category_id = request.POST.get("category")
#     subject_id = request.POST.get("subject")
#     set_id = request.POST.get("set")

#     if not uploaded_file or not category_id or not subject_id or not set_id:
#         return JsonResponse({"message": "File and all dropdown selections are required."}, status=400)

#     try:
#         category = get_object_or_404(Category, id=category_id, delflag=False)
#         subject = get_object_or_404(Subject, id=subject_id, category=category, delflag=False)
#         set_obj = get_object_or_404(Set, id=set_id, subject=subject, category=category, delflag=False)

#         # Ownership check
#         if set_obj.user != request.user:
#             return JsonResponse({"message": "Only the creator of the set can upload questions."}, status=403)

#         # Detect file type (CSV or Excel)
#         ext = uploaded_file.name.split(".")[-1].lower()
#         rows = []

#         if ext == "csv":
#             decoded_file = uploaded_file.read().decode("utf-8").splitlines()
#             reader = csv.DictReader(decoded_file)
#             rows = list(reader)
#         elif ext in ["xls", "xlsx"]:
#             df = pd.read_excel(uploaded_file)
#             rows = df.to_dict(orient="records")
#         else:
#             return JsonResponse({"message": "Unsupported file format. Use CSV or Excel."}, status=400)

#         # Save questions
#         for row in rows:
#             question_text = row.get("question_text", "").strip()
#             option_a = row.get("option_a", "").strip()
#             option_b = row.get("option_b", "").strip()
#             option_c = row.get("option_c", "").strip()
#             option_d = row.get("option_d", "").strip()
#             correct_option = row.get("correct_option", "").strip().lower()

#             if not all([question_text, option_a, option_b, option_c, option_d, correct_option]):
#                 continue  # Skip incomplete rows

#             # Check for soft-deleted duplicate
#             soft_deleted = Question.objects.filter(
#                 question_text=question_text,
#                 category=category,
#                 subject=subject,
#                 set=set_obj,
#                 user=request.user,
#                 delflag=True
#             ).first()

#             if soft_deleted:
#                 soft_deleted.option_a = option_a
#                 soft_deleted.option_b = option_b
#                 soft_deleted.option_c = option_c
#                 soft_deleted.option_d = option_d
#                 soft_deleted.correct_option = correct_option
#                 soft_deleted.delflag = False
#                 soft_deleted.save()
#             else:
#                 Question.objects.create(
#                     category=category,
#                     subject=subject,
#                     set=set_obj,
#                     user=request.user,
#                     question_text=question_text,
#                     option_a=option_a,
#                     option_b=option_b,
#                     option_c=option_c,
#                     option_d=option_d,
#                     correct_option=correct_option
#                 )

#         # ✅ Always fetch updated rows after processing
#         questions = Question.objects.select_related("category", "subject", "set", "user").filter(
#             user=request.user,
#             delflag=False
#         ).order_by('id')

#         html = render_to_string("partials/question_rows.html", {
#             "questions": questions,
#             "user_role": request.user.role,
#             "user": request.user,
#         }, request=request)

#         return JsonResponse({"message": "Questions uploaded successfully!", "html": html})


#     except Exception as e:
#         return JsonResponse({"message": str(e)}, status=500)

@jwt_required
@role_required('staff')
@require_http_methods(["GET", "POST"])
def upload_questions(request):
    if request.method == "GET":
        categories = Category.objects.filter(delflag=False)
        subjects = Subject.objects.filter(delflag=False)
        sets = Set.objects.filter(user=request.user, delflag=False)  # Only sets created by this staff

        # ✅ Load all existing questions for this staff
        questions = Question.objects.select_related("category", "subject", "set", "user").filter(
            user=request.user,
            delflag=False
        ).order_by('id')

        return render(request, "questions/csv_question_file_upload.html", {
            "categories": categories,
            "subjects": subjects,
            "sets": sets,
            "questions": questions,
            "user_role": request.user.role,
            "user": request.user,
        })

    # ✅ POST request — Handle file upload
    uploaded_file = request.FILES.get("file")
    category_id = request.POST.get("category")
    subject_id = request.POST.get("subject")
    set_id = request.POST.get("set")

    if not uploaded_file or not category_id or not subject_id or not set_id:
        return JsonResponse({"message": "File and all dropdown selections are required."}, status=400)

    try:
        category = get_object_or_404(Category, id=category_id, delflag=False)
        subject = get_object_or_404(Subject, id=subject_id, category=category, delflag=False)
        set_obj = get_object_or_404(Set, id=set_id, subject=subject, category=category, delflag=False)

        # ✅ Ownership check
        if set_obj.user != request.user:
            return JsonResponse({"message": "Only the creator of the set can upload questions."}, status=403)

        # ✅ Detect file type (CSV or Excel)
        ext = uploaded_file.name.split(".")[-1].lower()
        if ext == "csv":
            decoded_file = uploaded_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            rows = list(reader)
        elif ext in ["xls", "xlsx"]:
            df = pd.read_excel(uploaded_file)
            rows = df.to_dict(orient="records")
        else:
            return JsonResponse({"message": "Unsupported file format. Use CSV or Excel."}, status=400)

        # ✅ Save questions
        for row in rows:
            question_text = row.get("question_text", "").strip()
            option_a = row.get("option_a", "").strip()
            option_b = row.get("option_b", "").strip()
            option_c = row.get("option_c", "").strip()
            option_d = row.get("option_d", "").strip()
            correct_option = row.get("correct_option", "").strip().lower()

            if not all([question_text, option_a, option_b, option_c, option_d, correct_option]):
                continue  # Skip incomplete rows

            # Check for soft-deleted duplicate
            soft_deleted = Question.objects.filter(
                question_text=question_text,
                category=category,
                subject=subject,
                set=set_obj,
                user=request.user,
                delflag=True
            ).first()

            if soft_deleted:
                soft_deleted.option_a = option_a
                soft_deleted.option_b = option_b
                soft_deleted.option_c = option_c
                soft_deleted.option_d = option_d
                soft_deleted.correct_option = correct_option
                soft_deleted.delflag = False
                soft_deleted.save()
            else:
                Question.objects.create(
                    category=category,
                    subject=subject,
                    set=set_obj,
                    user=request.user,
                    question_text=question_text,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                    correct_option=correct_option
                )

        # ✅ Fetch ALL updated questions for this staff
        questions = Question.objects.select_related("category", "subject", "set", "user").filter(
            user=request.user,
            delflag=False
        ).order_by('id')

        # ✅ Render HTML table rows
        html = render_to_string("partials/question_rows.html", {
            "questions": questions,
            "user_role": request.user.role,
            "user": request.user,
        }, request=request)

        return JsonResponse({"message": "Questions uploaded successfully!", "html": html})

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)



@jwt_required
@role_required('staff')
@require_http_methods(["GET", "POST"])
def add_question(request):
    if request.method == "GET":
        categories = Category.objects.filter(delflag=False)
        subjects = Subject.objects.filter( delflag=False)
        sets = Set.objects.filter(user=request.user, delflag=False)

        # Get questions created by this staff only
        questions = Question.objects.select_related("category", "subject", "set", "user").filter(
            user=request.user,
            delflag=False
        )

        return render(request, "questions/add_questions.html", {
            "categories": categories,
            "subjects": subjects,
            "sets": sets,
            "questions": questions,
            "user_role": request.user.role,
            "user": request.user,
        })
    
    # POST request — Add Question logic
    data = request.POST
    question_text = data.get("question_text", "").strip()
    category_id = data.get("category")
    subject_id = data.get("subject")
    set_id = data.get("set")
    option_a = data.get("option_a", "").strip()
    option_b = data.get("option_b", "").strip()
    option_c = data.get("option_c", "").strip()
    option_d = data.get("option_d", "").strip()
    correct_option = data.get("correct_option", "").strip().lower()


    if not all([question_text, category_id, subject_id, set_id, option_a, option_b, option_c, option_d, correct_option]):
        return JsonResponse({"message": "All fields are required."}, status=400)

    try:
        category = get_object_or_404(Category, id=category_id, delflag=False)
        subject = get_object_or_404(Subject, id=subject_id, category=category, delflag=False)
        set_obj = get_object_or_404(Set, id=set_id, subject=subject, category=category, delflag=False)

        if set_obj.user != request.user:
            return JsonResponse({"message": "Only the creator of the set can add questions."}, status=403)

        # Check for soft-deleted duplicate
        soft_deleted = Question.objects.filter(
            question_text=question_text,
            category=category,
            subject=subject,
            set=set_obj,
            user=request.user,
            delflag=True
        ).first()

        if soft_deleted:
            soft_deleted.option_a = option_a
            soft_deleted.option_b = option_b
            soft_deleted.option_c = option_c
            soft_deleted.option_d = option_d
            soft_deleted.correct_option = correct_option
            soft_deleted.delflag = False
            soft_deleted.save()
        else:
            Question.objects.create(
                category=category,
                subject=subject,
                set=set_obj,
                user=request.user,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option
            )

        # Fetch updated question rows
        questions = Question.objects.select_related("category", "subject", "set", "user").filter(
            user=request.user,
            delflag=False
        )

        html = render_to_string("partials/question_rows.html", {
            "questions": questions,
            "user_role": request.user.role,
            "user": request.user,
        })

        return JsonResponse({"message": "Question added successfully!", "html": html})

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

# AJAX to get Subjects by Category
@jwt_required
@role_required('staff')
def get_subjects_by_category(request, category_id):
    subjects = Subject.objects.filter(category_id=category_id, delflag=False).values("id", "name")
    return JsonResponse({"subjects": list(subjects)})



@jwt_required
@role_required('staff')
def get_sets_by_subject(request, subject_id):
    sets = Set.objects.filter(subject_id=subject_id, user=request.user, delflag=False).values("id", "name")
    return JsonResponse({"sets": list(sets)})

# call from ajax for render in table 
@jwt_required
@role_required('staff')
def get_question_row(request, question_id):
    try:
        question = Question.objects.select_related("category", "subject", "set").get(id=question_id, delflag=False)

        if question.user != request.user:
            return JsonResponse({"message": "Permission denied."}, status=403)

        html = render_to_string("partials/question_rows.html", {
            "questions": [question],  # Single question in a list so the template loop works
            "user_role": request.user.role,
            "user": request.user,
        })

        return JsonResponse({"html": html})
    except Question.DoesNotExist:
        return JsonResponse({"message": "Question not found."}, status=404)



# @login_required
# @role_required('staff')  # Only staff allowed
# def question_list(request):
#     user = request.user

#     categories = Category.objects.filter(delflag=False)
#     subjects = Subject.objects.filter(delflag=False)
#     sets = Set.objects.filter(delflag=False, user=user)  # Staff sees only their sets
#     questions = Question.objects.select_related("category", "subject", "set", "user") \
#         .filter(delflag=False) \
#         .order_by("id")

#     return render(request, "questions/questions_list.html", {
#         "questions": questions,
#         "categories": categories,
#         "subjects": subjects,
#         "sets": sets,
#         "user_role": user.role,
#         "user": user,
#     })

@login_required
@role_required('staff')  # Only staff can access
def question_list(request):
    user = request.user

    # Get all non-deleted questions with related set, subject, and category
    questions = Question.objects.select_related(
        'set__subject', 'set__category', 'set__user'
    ).filter(delflag=False).order_by('id')

    return render(request, 'questions/questions_list.html', {
        'questions': questions,
        'user_role': user.role,
        "user": user,  # also used in the partial
    })


@jwt_required
@role_required('staff')
@require_POST
def edit_question(request, pk):
    question = get_object_or_404(Question, id=pk, delflag=False)

    if question.user != request.user:
        return JsonResponse({"message": "Unauthorized. You can only edit your own question."}, status=403)

    data = request.POST
    question_text = data.get("question_text", "").strip()
    category_id = data.get("category")
    subject_id = data.get("subject")
    set_id = data.get("set")
    option_a = data.get("option_a", "").strip()
    option_b = data.get("option_b", "").strip()
    option_c = data.get("option_c", "").strip()
    option_d = data.get("option_d", "").strip()
    correct_option = data.get("correct_option", "").strip()

    if not all([question_text, category_id, subject_id, set_id, option_a, option_b, option_c, option_d, correct_option]):
        return JsonResponse({"message": "All fields are required."}, status=400)

    try:
        category = Category.objects.get(id=category_id, delflag=False)
        subject = Subject.objects.get(id=subject_id, category=category, delflag=False)
        set_obj = Set.objects.get(id=set_id, subject=subject, category=category, delflag=False)

        if set_obj.user != request.user:
            return JsonResponse({"message": "Unauthorized. You can only assign your own set."}, status=403)

        # Update fields
        question.question_text = question_text
        question.category = category
        question.subject = subject
        question.set = set_obj
        question.option_a = option_a
        question.option_b = option_b
        question.option_c = option_c
        question.option_d = option_d
        question.correct_option = correct_option
        question.save()

        # Return updated question list HTML
        questions = Question.objects.select_related("category", "subject", "set", "user").filter(
            user=request.user, delflag=False
        )
        html = render_to_string("partials/question_rows.html", {
            "questions": questions,
            "user_role": request.user.role,
            "user": request.user
        }, request=request)

        return JsonResponse({"message": "Question updated successfully!", "html": html})

    except (Category.DoesNotExist, Subject.DoesNotExist, Set.DoesNotExist):
        return JsonResponse({"message": "Invalid category, subject, or set."}, status=400)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@jwt_required
@role_required('staff')
@require_POST
def delete_question(request, pk):
    question = get_object_or_404(Question, id=pk, delflag=False)

    if question.user != request.user:
        return JsonResponse({"message": "Unauthorized. You can only delete your own question."}, status=403)

    question.delflag = True
    question.save()

    questions = Question.objects.select_related("category", "subject", "set", "user").filter(
        user=request.user, delflag=False
    )
    html = render_to_string("partials/question_rows.html", {
        "questions": questions,
        "user_role": request.user.role,
        "user": request.user
    }, request=request)

    return JsonResponse({"message": "Question deleted successfully!", "html": html})


@login_required
@role_required('staff')
def question_recycle_bin(request):
    deleted_questions = Question.objects.select_related("category", "subject", "set", "user").filter(delflag=True)
    return render(request, "questions/recycle_bin.html", {
        "deleted_questions": deleted_questions,
        "user": request.user
    })


@jwt_required
@role_required('staff')
@require_POST
def restore_question(request, pk):
    question = get_object_or_404(Question, pk=pk, delflag=True)

    if question.user != request.user:
        return JsonResponse({"message": "You do not have permission to restore this question."}, status=403)

    question.delflag = False
    question.save()
    return JsonResponse({"message": "Question restored successfully."})

# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.views.decorators.http import require_GET, require_POST
# from .models import Subject, Set, Question, UserAnswer, Category
# from django.db.models import Count
# from account.decorators import jwt_required, role_required
# import random


# @jwt_required
# @role_required(['staff', 'student'])  # ✅ allow both roles
# @require_GET
# def home(request):
#     category_subject_map = {}
#     categories = Category.objects.filter(delflag=False)
#     for cat in categories:
#         category_subject_map[cat] = Subject.objects.filter(category=cat, delflag=False)
#     return render(request, 'home.html', {'category_subject_map': category_subject_map})

# @jwt_required
# @role_required(['staff', 'student'])  # ✅ shared start page
# @require_GET
# def start_test_page(request, subject_id):
#     subject = get_object_or_404(Subject, id=subject_id, delflag=False)
#     return render(request, 'start_test.html', {'subject': subject})


# @jwt_required
# @role_required(['staff', 'student'])  # ✅ assign random set
# @require_GET
# def assign_set(request):
#     subject_id = request.GET.get('subject_id')
#     subject = get_object_or_404(Subject, id=subject_id, delflag=False)

#     sets = Set.objects.filter(subject=subject, delflag=False).annotate(num_qs=Count('question')).filter(num_qs__gt=0)
#     if sets.exists():
#         selected_set = random.choice(list(sets))
#         UserAnswer.objects.filter(user=request.user, question__set=selected_set).delete()
#         return JsonResponse({'status': 'success', 'set_id': selected_set.id})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'No valid sets found for this subject.'})


# @jwt_required
# @role_required(['staff', 'student'])  # ✅ both can attempt quiz
# @require_GET
# def quiz_page(request):
#     return render(request, 'quiz.html')


# @jwt_required
# @role_required(['staff', 'student'])  # ✅ fetch question
# @require_GET
# def get_question(request):
#     set_id = request.GET.get('set_id')
#     if not set_id:
#         return JsonResponse({'status': 'error', 'message': 'Missing set ID'})

#     answered_ids = UserAnswer.objects.filter(user=request.user, question__set_id=set_id).values_list('question_id', flat=True)
#     question = Question.objects.filter(set_id=set_id, delflag=False).exclude(id__in=answered_ids).first()

#     if question:
#         return JsonResponse({
#             'status': 'success',
#             'question': {
#                 'id': question.id,
#                 'text': question.text,
#                 'options': [
#                     question.option1,
#                     question.option2,
#                     question.option3,
#                     question.option4
#                 ]
#             }
#         })
#     else:
#         return JsonResponse({'status': 'finished'})


# @jwt_required
# @role_required(['staff', 'student'])  # ✅ submit answer
# @require_POST
# def submit_answer(request):
#     qid = request.POST.get('question_id')
#     selected = request.POST.get('option')
#     question = get_object_or_404(Question, id=qid, delflag=False)

#     UserAnswer.objects.update_or_create(
#         user=request.user,
#         question=question,
#         defaults={'selected_option': selected}
#     )
#     return JsonResponse({'status': 'submitted'})


# @jwt_required
# @role_required(['staff', 'student'])  # ✅ show results
# @require_GET
# def show_result(request):
#     answers = UserAnswer.objects.filter(user=request.user)
#     correct = sum(1 for ans in answers if ans.selected_option == ans.question.correct)
#     return JsonResponse({'score': correct, 'total': answers.count()})



# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from .models import Subject, Set, Question, UserAnswer
# from django.contrib.auth.decorators import login_required
# from django.db.models import Count
# import random

# def home(request):
#     # Load all categories and subjects in one go
#     from .models import Category  # Assuming Category model
#     category_subject_map = {}
#     categories = Category.objects.filter(delflag=False)
#     for cat in categories:
#         category_subject_map[cat] = Subject.objects.filter(category=cat, delflag=False)
#     return render(request, 'home.html', {'category_subject_map': category_subject_map})

# @login_required
# def start_test_page(request, subject_id):
#     subject = get_object_or_404(Subject, id=subject_id, delflag=False)
#     return render(request, 'start_test.html', {'subject': subject})

# @login_required
# def assign_set(request):
#     subject_id = request.GET.get('subject_id')
#     subject = get_object_or_404(Subject, id=subject_id, delflag=False)

#     # Random set for logged-in staff-created ones
#     sets = Set.objects.filter(subject=subject, delflag=False).annotate(num_qs=Count('question')).filter(num_qs__gt=0)
#     if sets.exists():
#         selected_set = random.choice(list(sets))
#         request.user.useranswer_set.filter(question__set=selected_set).delete()  # fresh start
#         return JsonResponse({'status': 'success', 'set_id': selected_set.id})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'No valid sets with questions.'})

# @login_required
# def quiz_page(request):
#     return render(request, 'quiz.html')

# @login_required
# def get_question(request):
#     set_id = request.GET.get('set_id')
#     answered = UserAnswer.objects.filter(user=request.user, question__set_id=set_id).values_list('question_id', flat=True)
#     question = Question.objects.filter(set_id=set_id, delflag=False).exclude(id__in=answered).first()
#     if question:
#         return JsonResponse({
#             'status': 'success',
#             'question': {
#                 'id': question.id,
#                 'text': question.text,
#                 'options': [question.option1, question.option2, question.option3, question.option4]
#             }
#         })
#     else:
#         return JsonResponse({'status': 'finished'})

# @login_required
# def submit_answer(request):
#     qid = request.POST.get('question_id')
#     answer = request.POST.get('option')
#     question = get_object_or_404(Question, id=qid, delflag=False)
#     UserAnswer.objects.update_or_create(
#         user=request.user,
#         question=question,
#         defaults={'selected_option': answer}
#     )
#     return JsonResponse({'status': 'submitted'})

# @login_required
# def show_result(request):
#     answers = UserAnswer.objects.filter(user=request.user)
#     correct = sum(1 for ans in answers if ans.selected_option == ans.question.correct)
#     return JsonResponse({'score': correct, 'total': answers.count()})
from django.shortcuts import render
from django.http import JsonResponse
from .models import Question, UserAnswer
from question_sets.models import Set
from subject.models import Subject
from questions.models import Attempt
import random
from django.views.decorators.http import require_GET, require_POST
from account.decorators import jwt_required, role_required  # Adjust path to your decorators

# ---------- 1. Start Test Page ----------
@jwt_required
@role_required('student')  # or allow both staff & students if needed
@require_GET
def start_test_page(request):
    subjects = Subject.objects.filter(delflag=False)
    return render(request, 'questions/start_test.html', {'subjects': subjects})

# @jwt_required
# @role_required('student')
# @require_GET
# def assign_random_set(request):
#     subject_id = request.GET.get('subject_id')
#     user = request.user

#     sets = Set.objects.filter(subject_id=subject_id, delflag=False)
#     if not sets.exists():
#         return JsonResponse({'status': 'fail', 'message': 'No sets available for this subject.'})

#     random_set = random.choice(sets)

#     attempt = Attempt.objects.create(user=user, set=random_set)

#     return JsonResponse({
#         'status': 'success',
#         'set_id': random_set.id,
#         'attempt_id': attempt.id  # include this in the response
#     })
@jwt_required
@role_required('student')
@require_GET
def assign_random_set(request):
    subject_id = request.GET.get('subject_id')
    user = request.user

    print("Assigning set for subject_id:", subject_id, "| user:", user)

    sets = Set.objects.filter(subject_id=subject_id, delflag=False)
    if not sets.exists():
        return JsonResponse({'status': 'fail', 'message': 'No sets available for this subject.'})

    random_set = random.choice(list(sets)) #Python-এর random.choice() ফাংশন list (বা tuple)-এর উপরই কাজ করে,
    #                               কিন্তু Django-এর QuerySet একটা lazy iterable — সরাসরি সেটা random.choice() কে দিলে ভুল ফলাফল বা Error দিতে পারে।
    attempt = Attempt.objects.create(user=user, set=random_set) 

    print("Assigned set:", random_set.id, "| Attempt ID:", attempt.id)

    return JsonResponse({
        'status': 'success',
        'set_id': random_set.id,
        'attempt_id': attempt.id 
    })


# # ---------- 3. Get Next Question ----------
# @jwt_required
# @role_required('student')
# @require_GET
# def get_question(request):
#     set_id = request.GET.get('set_id')
#     attempt_id = request.GET.get('attempt_id')
#     user = request.user

#     attempt = Attempt.objects.get(id=attempt_id, user=user)
#     answered_qs = UserAnswer.objects.filter(attempt=attempt).values_list('question_id', flat=True)

#     next_q = Question.objects.filter(set_id=set_id, delflag=False).exclude(id__in=answered_qs).first()

#     if not next_q:
#         return JsonResponse({'status': 'completed'})

#     options = {
#         'A': next_q.option_a,
#         'B': next_q.option_b,
#         'C': next_q.option_c,
#         'D': next_q.option_d,
#     }

#     return JsonResponse({
#         'status': 'success',
#         'question_id': next_q.id,
#         'text': next_q.question_text,
#         'options': options
#     })

@jwt_required
@role_required('student')
@require_GET
def get_question(request):
    set_id = request.GET.get('set_id')
    attempt_id = request.GET.get('attempt_id')
    user = request.user

    print("Getting next question for set:", set_id, "| attempt:", attempt_id)

    try:
        attempt = Attempt.objects.get(id=attempt_id, user=user)
    except Attempt.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'Invalid attempt.'})

    answered_qs = UserAnswer.objects.filter(attempt=attempt).values_list('question_id', flat=True)
    print("Answered questions:", list(answered_qs))

    next_q = Question.objects.filter(set_id=set_id, delflag=False).exclude(id__in=answered_qs).first()

    if not next_q:
        print("All questions completed.")
        return JsonResponse({'status': 'completed'})

    options = {
        'A': next_q.option_a,
        'B': next_q.option_b,
        'C': next_q.option_c,
        'D': next_q.option_d,
    }

    print("Next question ID:", next_q.id)

    return JsonResponse({
        'status': 'success',
        'question_id': next_q.id,
        'text': next_q.question_text,
        'options': options
    })

@jwt_required
@role_required('student')
@require_POST
def submit_answer(request):
    user = request.user

    question_id = request.POST.get('question_id')
    selected_option = request.POST.get('selected_option')
    attempt_id = request.POST.get('attempt_id')

    selected_option = request.POST.get('selected_option', '').strip()
    if not question_id or not attempt_id:
        return JsonResponse({'error': 'Missing data'}, status=400)

    # Handle unanswered (no option selected)
    if selected_option not in ['A', 'B', 'C', 'D']:
        selected_option = None


    try:
        question = Question.objects.get(pk=question_id)
        attempt = Attempt.objects.get(pk=attempt_id)

        is_correct = selected_option == question.correct_option

        UserAnswer.objects.create(
            user=user,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            attempt=attempt
        )

        return JsonResponse({
            "message": "Answer submitted",
            "correct_option": question.correct_option,
            'question': question.question_text,  # ✅ CORRECT

            "is_correct": is_correct
        }, status=201)

    except Question.DoesNotExist:
        return JsonResponse({"error": "Question not found"}, status=404)
    except Attempt.DoesNotExist:
        return JsonResponse({"error": "Attempt not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
        
