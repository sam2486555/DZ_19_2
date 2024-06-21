from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Blog


def home(request):
    return render(request, 'home.html')


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            print(f'You have new message from {name} ({phone}): {message}')
        return render(request, template_name='catalog/contacts.html')


# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'{name} {phone} {message}')
#     return render(request, 'contacts.html')

class ProductsListview(ListView):
    model = Product


# def products_list(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, 'product_list.html', context)

class ProductsDetailview(DetailView):
    model = Product

# def products_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, 'products_detail.html', context)

class BlogListview(ListView):
    template_name = 'blog/blog_list.html'
    model = Blog
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogDetailview(DetailView):
    template_name = 'blog/blog_detail.html'
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    template_name = 'blog/blog_form.html'
    model = Blog
    fields = ('title', 'slug', 'content', 'preview', 'created_at')
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    template_name = 'blog/blog_form.html'
    model = Blog
    fields = ('title', 'slug', 'content', 'preview', 'created_at')

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=(self.kwargs.get('pk'),))


class BlogDeleteView(DeleteView):
    template_name = 'blog/blog_delete.html'
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')