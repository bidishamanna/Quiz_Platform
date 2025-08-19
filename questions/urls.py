# from django.urls import path
# from . import views

# urlpatterns=[
#     # path("", views.question_list, name="question_list"),
#     # path('add_question/', views.add_question, name='add_question'),
#     # path("edit_question/<int:pk>/", views.edit_question, name="edit_question"),
#     # path('delete_question/<int:pk>/',views.delete_question,name= 'delete_question'),

    
#     path("questions/", views.add_question_page, name="add_question"),
#     path("add/", views.add_question_ajax, name="add-question-ajax"),



#     # # questions
#     # path('add_questions/', views.add_questions, name='add_questions'),
#     # path('start_test/', views.start_test, name='start_test'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_question, name='add_question'),
    path('get_subjects/<int:category_id>/', views.get_subjects_by_category, name='get_subjects_by_category'),
    path('get_sets/<int:subject_id>/', views.get_sets_by_subject, name='get_sets_by_subject'),
    path('list/', views.question_list, name='question_list'),
    path('get_row/<int:question_id>/', views.get_question_row, name='get_question_row'), # for table display 
    path('edit/<int:pk>/', views.edit_question, name='edit_question'),
    path('delete/<int:pk>/', views.delete_question, name='delete_question'),
     # ♻️ Recycle Bin for Questions (Page View)
    path('recycle_bin/', views.question_recycle_bin, name='question_recycle_bin'),

    # 🔁 Restore Deleted Question (AJAX POST)
    path('restore/<int:pk>/', views.restore_question, name='restore_question'),


    # for start test -- 

    # urls.py (app level or project level if included)
    # path('start-test/', views.start_test, name='start_test'),
    # path('test/', views.test_page, name='test_page'),
    # path('assign-random-set/', views.assign_random_set, name='assign_random_set'),
    # path('get-question/', views.get_question, name='get_question'),
    # path('submit-answer/', views.submit_answer, name='submit_answer'),

    # path('start-test/', views.start_test, name='start_test'),
    # path('test/', views.test_page, name='test_page'),
    # path('assign-random-set/', views.assign_random_set, name='assign_random_set'),
    # path('get-question/', views.get_question, name='get_question'),
    # path('submit-answer/', views.submit_answer, name='submit_answer'),

    path('start/', views.start_test_page, name='start_test'),
    path('assign-random-set/', views.assign_random_set, name='assign_random_set'),
    path('get-question/', views.get_question, name='get_question'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),

    
    path('upload-questions/', views.upload_questions, name='upload_questions'),





]



