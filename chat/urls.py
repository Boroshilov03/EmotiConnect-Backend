from django.urls import path
from .views import SignInView, SignUpView, TestView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('test/', TestView.as_view())
]