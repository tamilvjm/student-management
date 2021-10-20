from django.urls import path
from student_app.auth1.views import ListCourseHistory, MyObtainTokenPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from student_app.auth1.views import ChangePasswordView, UpdateProfileView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('course-history/', ListCourseHistory.as_view(), name='course_history'),
]