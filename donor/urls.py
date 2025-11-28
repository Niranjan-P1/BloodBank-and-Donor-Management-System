from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_donor, name='register_donor'),
    path('requests/', views.blood_request, name='blood_request'),
    path('reports/', views.reports_page, name='reports_page'),
    path('export/filtered-report/pdf/', views.export_filtered_report_pdf, name='export_filtered_report_pdf'),
    path("about/", views.about, name="about"),
    path("manage/requests/", views.manage_requests, name="manage_requests"),

    # auth
    path("login/", auth_views.LoginView.as_view(template_name="donor/login.html"), name="login"),

    # Ensure explicit redirect to home after logout
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("home")), name="logout"),
]
