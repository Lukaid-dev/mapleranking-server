from django.contrib import admin
from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

import os

ENTRY_PORT = int(os.environ.get("ENTRY_PORT", default=3030))

urlpatterns = [
    path("admin/", admin.site.urls),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Maple Ranking API",
        default_version="v1",
        description="""
        Maple Ranking API 문서입니다.
        작성자 : 이성우
        """,
        terms_of_service="",
        contact=openapi.Contact(name="이성우", email="crescent3859@gmail.com"),
        license=openapi.License(name="maple_ranking_api_docs"),
    ),
    url=f"http://lukaid.iptime.org:{ENTRY_PORT}/",
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
)

urlpatterns += [
    path(
        "swagger<str:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += [
    path("api/v1/a_test/", include("apps.commons.urls")),
    path("api/v1/auth/", include("apps.users.urls")),
]
