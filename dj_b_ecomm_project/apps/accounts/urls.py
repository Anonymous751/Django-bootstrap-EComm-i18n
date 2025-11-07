# Import Django's 'path' function to define URL patterns
from django.urls import path

# Import views from the current application
from . import views

app_name = 'accounts'

# Define all URL patterns for this app
urlpatterns = [
    # User authentication routes
    path('register/', views.register_view, name='register'),  # URL for user registration
    
    
    # path('activate/<uidb64>/<token>/', views.activate_account, name='activate'), uncomment when you want to send email
    
    path('login/', views.login_view, name='login'),            # URL for user login # type: ignore
    path('logout/', views.logout_view, name='logout'),          # URL for logging out the user

    # Dashboard route (requires authentication)
    path('dashboard/', views.dashboard_view, name='dashboard'), # URL for user dashboard

    # Admin-specific settings route
    # Note: using 'as_view()' indicates this is a class-based view
    path('admin-settings/', views.admin_settings_view, name='admin_settings'),
    
    # Private account?
    path("profile/<str:username>/", views.profile_view, name="profile"),
    
    path('update-privacy-security/', views.update_privacy_security, name='update_privacy_security'), # type: ignore
    
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    
    
    # password reset ?
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    
    path('verify-reset-otp/', views.verify_reset_otp_view, name='verify_reset_otp'),
    
    path('reset-password/', views.reset_password_view, name='reset_password'),
    
    
    # advanced analytics
     path("analytics/advanced/", views.advanced_analytics, name="advanced_analytics"),
     
    path("sales-report/", views.sales_report, name="sales_report"),
    
    path("user-traffic/", views.user_traffic, name="user_traffic"),
    
    path("ai-predictions/", views.ai_predictions, name="ai_predictions"),

    # Theme url 
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),

] 
