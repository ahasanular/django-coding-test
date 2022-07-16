from django.http import JsonResponse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from product.models import Product, ProductVariant, ProductVariantPrice, Variant

# end of import


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


# This is for saving those data come from frontend ***** UNFINISHED *******
# This do not work. It only get those data and assign new product and product variant table but don't SAVE.
class AddProductView(generic.CreateView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST

            print("print data")
            print(data)

            product = Product(title=data['title'], sku=data['sku'], description=data['description'])
            # product.save()

            product_variant_all = []
            product_variant = ProductVariant(variant_title=data['product_variant[0][tags][]'],
                                             variant=Variant.objects.filter(id=data['product_variant[0][option]']).first(),
                                             product=product)
            # product_variant.save()
            product_variant_all.append(product_variant)

            return JsonResponse({'message': 'success'})

        except Exception as ex:
            return JsonResponse({'message': str(ex)})


# This is for the List view of all products and their variants and details *** WORKS FINE ***
class ListProductView(generic.ListView):
    template_name = 'products/list.html'
    model = Product
    paginate_by = 5
    no_pagination = False
    no_pagination_url = ''
    my_var = []

    def get_context_data(self, **kwargs):
        context = super(ListProductView, self).get_context_data(**kwargs)

        title = self.request.GET.get('title')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')
        variant = self.request.GET.get('variant')

        queryset1 = ProductVariantPrice.objects.filter().all().order_by('id')

        if title:
            queryset1 = queryset1.filter(product__title__icontains=title).all()
        if price_from:
            queryset1 = queryset1.filter(price__gte=price_from).all()
        if price_to:
            queryset1 = queryset1.filter(price__lte=price_to)
        if date:
            queryset1 = queryset1.filter(product__created_at__year=date.split('-')[0],
                                         product__created_at__month=date.split('-')[1])
        if variant:
            queryset1 = queryset1.filter(Q(product_variant_one__variant_title__iexact=variant) |
                                         Q(product_variant_two__variant_title__iexact=variant) |
                                         Q(product_variant_three__variant_title__iexact=variant))
        # Copying all the product id that filtered from product variant price
        self.my_var = []
        for i in queryset1:
            self.my_var.append(i.product.id)
        self.my_var = sorted(set(self.my_var))

        # qurying from product model only those are in filtered product variants too and updating the contex
        context.update(product_list=Product.objects.filter(id__in=self.my_var))

        page = self.request.GET.get('page')

        # declaring paginator on what queryset it should work
        paginator = Paginator(context['product_list'], self.paginate_by)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        context.update(product_variants=queryset1)
        context.update(product_list=data)

        return context

