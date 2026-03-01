"""
Root URL configuration for Task Management API.

Routes:
    /admin/          – Django admin panel
    /api/            – Authentication endpoints (register, login, logout)
    /api/            – Task CRUD endpoints
    /api/docs/       – Swagger UI
    /api/schema/     – OpenAPI schema (YAML)
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("admin/", admin.site.urls),
    # Auth endpoints
    path("api/", include("users.urls")),
    # Task endpoints
    path("api/", include("tasks.urls")),
    # OpenAPI schema & Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
