
from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "api/calculate-age/",
        api_views.calculate_age_api,
        name="calculate_age_api"
    ),
]
