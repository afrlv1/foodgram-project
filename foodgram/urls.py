import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", include("django.contrib.flatpages.urls")),
    path("about-author/", views.flatpage, {"url": "/about-author/"}, name="about-author"),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="about-spec"),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("api/", include("api.urls")),
    path("", include("recipes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

handler404 = "recipes.views.page_not_found"  # noqa
handler500 = "recipes.views.server_error"  # noqa
