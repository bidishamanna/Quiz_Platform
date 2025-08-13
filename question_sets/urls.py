from django.urls import path
from . import views

urlpatterns=[
    path("", views.set_list, name="set_list"),
    path('add/', views.add_set, name='add_set'),
    path("edit/<int:pk>/", views.edit_set, name="edit_set"),
    path("delete/<int:pk>/", views.delete_set, name="delete_set"),
    path("get_subjects/", views.get_subjects, name="get_subjects"),#----only selected category show their subject 
    path('get_rows/',views.get_set_rows,name = 'get_set_rows'),
    # path("recycle_bin/", views.recycle_bin, name="recycle_bin"), 
    # path("restore/<int:pk>/", views.restore_category, name="restore_category"),
    path("recycle-bin/", views.set_recycle_bin, name="set_recycle_bin"),
    path("restore/<int:pk>/", views.restore_set, name="restore_set"),
]


