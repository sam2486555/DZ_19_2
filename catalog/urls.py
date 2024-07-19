from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ContactsView, BlogCreateView, BlogUpdateView, \
    BlogListview, BlogDetailview, BlogDeleteView, \
    ProductListview, ProductDetailview, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('', ProductListview.as_view(), name='product_list'),
    path('category', CategoryListView.as_view(), name='category_list'),
    path('products/<int:pk>/', cache_page(60)(ProductDetailview.as_view()), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('blog/', BlogListview.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailview.as_view(), name='blog_detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),

]
