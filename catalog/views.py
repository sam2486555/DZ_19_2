from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm, BlogForm, BlogModeratorForm
from catalog.models import Product, Blog, Version


# def home(request):
#     return render(request, 'home.html')


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            print(f'You have new message from {name} ({phone}): {message}')
        return render(request, template_name='catalog/contacts.html')


class ProductListview(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = self.get_queryset(*args, **kwargs)

        for product in products:
            versions = Version.objects.filter(product=product)
            active_versions = versions.filter(current_version=True)
            if active_versions:
                product.active_version = active_versions.last().version_title
            else:
                product.active_version = 'Нет активной версии'

        context_data['object_list'] = products
        return context_data


class ProductDetailview(DetailView):
    model = Product


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.user = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=(self.kwargs.get('pk'),))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return ProductForm
        if user.has_perm(
            "catalog.can_canceled_public") and user.has_perm(
            "catalog.can_edit_desk") and user.has_perm(
            "catalog.can_edit_category"):
            return ProductModeratorForm

        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'catalog/product_delete.html'
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.view_counter += 1
            self.object.save()
            return self.object
        raise PermissionDenied()

    # def delete_product(request, product_id):
    #
    #     product = get_object_or_404(Product, pk=product_id)
    #
    #     if request.user.has_perm('app.delete_product') or request.user == product.owner or request.user.is_superuser:
    #
    #         product.delete()
    #
    #         return redirect('products_list')
    #
    #     else:
    #
    #         raise PermissionDenied


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


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/blog_form.html'
    model = Blog
    fields = ('title', 'slug', 'content', 'preview', 'created_at')

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=(self.kwargs.get('pk'),))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return BlogForm
        if user.has_perm("catalog.can_edit"):
            return BlogModeratorForm
        raise PermissionDenied


class BlogDeleteView(DeleteView):
    template_name = 'blog/blog_delete.html'
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
