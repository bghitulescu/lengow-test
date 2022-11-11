from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_orders, name="list_orders"),
    path("<str:order_id>/", views.order_details, name="order_details"),
]
