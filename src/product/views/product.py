from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Prefetch
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from product.models import Product, ProductVariant, ProductVariantPrice, Variant
from product.serializers import ProductSerializer

import json

# end of import
from rest_framework.response import Response


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


# This is for saving those data come from frontend ***** UNFINISHED *******
#               ONLY SAVE PRODUCT MODEL
# This does not work. It only gets those data and assign new product and product variant, but don't SAVE everything.
# class AddProductView(generic.CreateView):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body)
#
#             product = Product(title=data['title'], sku=data['sku'], description=data['description'])
#
#             product_variant = []
#             for dt in data['product_variant']:
#                 product_variant.append(ProductVariant(variant_title=dt['tags'],
#                                                       variant=Variant.objects.filter(id=dt['option']).first(),
#                                                       product=product))
#
#             product_variant_price = ProductVariantPrice(product_variant_one=product_variant[0],
#                                                         product_variant_two=product_variant[0],
#                                                         product_variant_three=product_variant[0],
#                                                         product=product,
#                                                         )
#             product_variant_price = []
#             for dt in data['product_variant_prices']:
#                 title = dt['title'].split('/')
#                 product_variant_price.append(
#                     ProductVariantPrice(
#                         product_variant_one=title[0],
#                         product_variant_two=title[1],
#                         product_variant_three=title[2],
#                         product=product,
#                         price=dt['price'],
#                         stock=dt['stock'],
#                     )
#                 )
#
#             print("print data")
#             print(data)
#             print("print data Type")
#             print(type(data))
#             print("print data Vars")
#             # print(vars(data))
#             print("print data dir")
#             print(dir(data))
#
#             product = Product(title=data['title'], sku=data['sku'], description=data['description'])
#             product.save()
#
#             product_variant_all = []
#             product_variant = ProductVariant(variant_title=data['product_variant[0][tags][]'],
#                                              variant=Variant.objects.filter(
#                                                  id=data['product_variant[0][option]']).first(),
#                                              product=product)
#             # product_variant.save()
#             product_variant_all.append(product_variant)
#
#             return JsonResponse({'message': 'success'})
#
#         except Exception as ex:
#             print("ERROR FOUND")
#             print(str(ex))
#             return JsonResponse({'message': str(ex)})


class AddProductView(generic.CreateView):
    def post(self, request, *args, **kwargs):
        feedback = {}
        try:
            data = json.loads(request.body)

            if 'title' not in data or 'sku' not in data:
                feedback['message'] = "Product TITLE or SKU or VARIANT or VARIANT PRICE data not found"
                feedback['status'] = HTTP_400_BAD_REQUEST
                return JsonResponse(feedback)
            if data['title'] == '' or data['sku'] == '':
                feedback['message'] = "Product Title or SKU can not be empty"
                feedback['status'] = HTTP_400_BAD_REQUEST
                return JsonResponse(feedback)
            if len(data['product_variant_prices']) == 0:
                feedback['message'] = "Product variant Prices Data can't be empty"
                feedback['status'] = HTTP_400_BAD_REQUEST
                return JsonResponse(feedback)

            product = Product.objects.filter(sku=data['sku']).first()

            if not product:
                product = Product(title=data['title'], sku=data['sku'], description=data['description'])
                product.save()

            # product_variant = []
            for dt in data['product_variant']:
                for tags in dt['tags']:
                    single_product_variant = ProductVariant(variant_title=tags,
                                                            variant=Variant.objects.filter(id=dt['option']).first(),
                                                            product=product)
                    single_product_variant.save()

                    # product_variant.append(single_product_variant)

            # product_variant_price = []
            for dt in data['product_variant_prices']:
                title = dt['title'].split('/')
                single_product_variant_price = ProductVariantPrice(
                    product_variant_one=ProductVariant.objects.filter(variant_title=title[0], product=product).first(),
                    product_variant_two=ProductVariant.objects.filter(variant_title=title[1], product=product).first(),
                    product_variant_three=ProductVariant.objects.filter(variant_title=title[2],
                                                                        product=product).first(),
                    product=product,
                    price=dt['price'],
                    stock=dt['stock'],
                )

                single_product_variant_price.save()

                # product_variant_price.append(single_product_variant_price)

            # print("", end='\n\n')
            #
            # for i in data['product_variant_prices']:
            #     print(i['title'])
            #
            # print("", end='\n\n')
            #
            # print("print data")
            # print(data)
            # print("print data Type")
            # print(type(data))
            # print("print data Vars")
            # # print(vars(data))
            # print("print data dir")
            # print(dir(data))
            #
            # print("<<<<<<<<<<<<<<<<<<<< END OF FRONT END >>>>>>>>>>>>>>>>>>>>>>>")
            # print("print product")
            # print(product)
            # print("print product Type")
            # print(type(product))
            # print("print product Vars")
            # # print(vars(product))
            # print("print product dir")
            # print(dir(product))

            feedback['message'] = "successfully inserted product, product variant and product variant prices"
            feedback['status'] = HTTP_200_OK
            return JsonResponse(feedback)

        except Exception as ex:
            print("ERROR FOUND")
            print(str(ex))
            feedback['message'] = "Exception happen : " + str(ex)
            feedback['status'] = HTTP_400_BAD_REQUEST
            return JsonResponse(feedback)


# Making Product list with all variant and price stock details and showing by paginated
#                                 ********Using REST FRAMEWORK********
class ListProductView(ListAPIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            title = request.GET.get('title')
            price_from = request.GET.get('price_from')
            price_to = request.GET.get('price_to')
            date = request.GET.get('date')
            variant = request.GET.get('variant')

            product_variant_price = ProductVariantPrice.objects.filter()  # get productVariantPrice data for filtering

            if price_from:  # Checkin if price_from exists in query params
                product_variant_price = product_variant_price.filter(price__gte=price_from)
            if price_to:  # Checkin if price_to exists in query params
                product_variant_price = product_variant_price.filter(price__lte=price_to)
            if variant:  # Checkin if variant exists in query params
                product_variant_price = product_variant_price.filter(
                    Q(product_variant_one__variant_title__iexact=variant) |
                    Q(product_variant_two__variant_title__iexact=variant) |
                    Q(product_variant_three__variant_title__iexact=variant)
                )

            # making a list of product id that exist after filter
            product_variant_price_id = []
            for dt in product_variant_price:
                product_variant_price_id.append(dt.product.id)

            # making the main queryset by filtering product by the list and prefetch product_variant_price queryset
            queryset = Product.objects.filter(id__in=product_variant_price_id).prefetch_related(
                Prefetch('productVariantPrice', product_variant_price)
            )

            # After getting the queryset filtering products for the product title and the data
            if title:  # Checkin if title exists in query params
                queryset = queryset.filter(title__icontains=title)
            if date:  # Checkin if date exists in query params
                queryset = queryset.filter(created_at__year=date.split('-')[0],
                                           created_at__month=date.split('-')[1])

            # serializing the main queryset
            serializer = ProductSerializer(queryset, many=True)

            page = request.GET.get('page')

            # declaring paginator on what queryset it should work
            paginator = Paginator(serializer.data, 5)
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)

            serializer = data

            return render(request, 'products/list.html', {'data': serializer})
        except Exception as ex:
            return render(request, 'products/list.html', str(ex))