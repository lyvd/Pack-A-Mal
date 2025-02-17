from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("", views.dashboard, name="dashboard"),
    path("get_wolfis_packages/", views.get_wolfis_packages, name="get_wolfis_packages"),
    path("submit/", views.submit, name="submit"),
    path("configure/", views.configure, name="configure"),
    path("analyze/", views.analyze, name="analyze"),
    path("results/", views.results, name="results"),
    path("upload/", views.upload, name="upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
