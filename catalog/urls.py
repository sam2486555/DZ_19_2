from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ContactsView, ProductsListview, ProductsDetailview, BlogCreateView, BlogUpdateView, \
    BlogListview, BlogDetailview, BlogDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('', ProductsListview.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductsDetailview.as_view(), name='products_detail'),
    path('blog/', BlogListview.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailview.as_view(), name='blog_detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),

]
