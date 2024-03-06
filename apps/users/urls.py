from django.urls import path

from apps.users import views


urlpatterns = [
    path("me/", views.Me.as_view(), name="me"),
    path("logout/", views.Logout.as_view(), name="logout"),
    # path("delete/", views.UserDelete.as_view(), name="delete"),
]
