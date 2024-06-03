from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, products_list, products_detail

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('', products_list, name='products_list'),
    path('products/<int:pk>/', products_detail, name='products_detail')

]
