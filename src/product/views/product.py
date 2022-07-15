from django.views import generic

from product.models import Product, ProductVariant, ProductVariantPrice, Variant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ListProductView(generic.ListView):
    template_name = 'products/list.html'

    def get_queryset(self):
        queryset = Product.objects.filter().all()
        print("DS")
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        return context