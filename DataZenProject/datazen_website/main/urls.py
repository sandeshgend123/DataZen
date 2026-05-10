from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('contact/<int:contact_id>/mark-read/', views.mark_contact_read, name='mark_contact_read'),
    path('contact/<int:contact_id>/reply/', views.send_contact_reply, name='send_contact_reply'),
    path('contact/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('admin-dashboard/', views.admin_profile, name='admin_profile'),
    path('mark-inquiry-read/<int:inquiry_id>/', views.mark_inquiry_read, name='mark_inquiry_read'),
    path('select-plan/', views.select_plan, name='select_plan'),
    path('sales-department/', views.sales_department, name='sales_department'),
    path('sales-department/<str:plan>/', views.sales_department, name='sales_department_plan'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]
