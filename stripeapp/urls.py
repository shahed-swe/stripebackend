
from django.urls import path
from .views import purchase_product,manage_payment_methods,add_payment_method

urlpatterns = [
    # path('make_payment/', make_payment, name='make_payment'),
    # path('retrieve-cards/', retrieve_cards, name='retrieve_cards'),
    path('purchase/', purchase_product, name='purchase_product'),
    path('payment_methods/', manage_payment_methods, name='manage_payment_methods'),
    path('add_payment_method/', add_payment_method, name='add_payment_method'),
]