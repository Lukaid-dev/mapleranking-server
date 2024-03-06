from django.urls import path
from apps.commons.views import Test

urlpatterns = [
    path("", Test.as_view(), name="test"),
]
