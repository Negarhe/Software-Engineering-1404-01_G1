from django.urls import path
from . import views

urlpatterns = [
    path("", views.base),
    path("ping/", views.ping),
    path("exams/", views.exam),
    path("speaking/", views.speaking_exam),
    path("feedbacks/", views.feedback),
]