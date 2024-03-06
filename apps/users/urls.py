from django.urls import path

from apps.users import views


urlpatterns = [
    path("me/", views.Me.as_view(), name="me"),
    # path("login/", views.Login.as_view(), name="login"),
    # path("logout/", views.Logout.as_view(), name="logout"),
    # path("delete/", views.UserDelete.as_view(), name="delete"),
]
