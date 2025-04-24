from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

app_name = "main"

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update-cart/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/checkout", views.checkout, name="checkout"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
