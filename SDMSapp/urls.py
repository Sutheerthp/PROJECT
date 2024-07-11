from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
    path('add_student/', add_student, name='add_student'),
    path('assign_student/', assign_student, name='assign_student'),
    path('confirm_assign_delete/<int:stud_id>/', confirm_assign_delete, name='confirm_assign_delete'),
    path('success_page/', success_page, name='success_page'),
    path('edit_student_form/', edit_student_form, name='edit_student_form'),
    path('edit_student/<str:uty_reg_no>/', edit_student, name='edit_student'),
    path('delete_student/<str:uty_reg_no>/', delete_student, name='delete_student'),
    path('confirm_delete_student/<str:uty_reg_no>/', confirm_delete_student, name='confirm_delete_student'),
    path('view_student/', view_student, name='view_student'),
    path('assignview_student/', assignview_student, name='assignview_student'),
    path('view_items/', view_items, name='view_items'),
    path('view_players/<int:item_id>/', view_players, name='view_players'),
    path('search_student/', search_student, name='search_student'),
    path('edit_assignment/<int:pk>/', edit_assignment, name='edit_assignment'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('view_attendance/', view_attendance, name='view_attendance'),
    path('delete_attendance/<int:attendance_id>/', delete_attendance, name='delete_attendance'),
    path('upload_picture/', upload_picture, name='upload_picture'),
    path('view_pictures/', view_pictures, name='view_pictures'),
    path('download_picture/<int:picture_id>/', download_picture, name='download_picture'),
    path('assign_players/', assign_players, name='assign_players'),
    path('view_profile/<str:uty_reg_no>/', view_profile, name='view_profile'),
    path('manage_certificate/', manage_certificate, name='manage_certificate'),
    path('certificate_list/', certificate_list, name='certificate_list'),
    path('edit_certificate/<int:certificate_id>/', edit_certificate, name='edit_certificate'),
    path('delete_certificate/<int:certificate_id>/', delete_certificate, name='delete_certificate'),
    path('student_grace_marks/', student_grace_marks, name='student_grace_marks'),
    path('get_items_by_student/', get_items_by_student, name='get_items_by_student'),
    path('get_student_details/', get_student_details, name='get_student_details'),
]