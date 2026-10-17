from django.contrib import admin
from django.urls import include, path
from restaurant.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("api/menu/", include("restaurant.menu_urls")),
    path("api/booking/", include("restaurant.booking_urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
