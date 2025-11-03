from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_orders, name="orders_show"),
    path("orders/new/", views.orders_new, name="orders_new"),
    path("orders/<int:oid>/edit/", views.orders_edit, name="orders_edit"),
    path("orders/<int:oid>/delete/", views.orders_delete, name="orders_delete"),
]