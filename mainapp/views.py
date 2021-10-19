import operator

from functools import reduce
from itertools import chain
import requests
import datetime
import json

from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.views.generic import DetailView, View
from django.urls import reverse
from django.contrib.auth import login, authenticate
from openpyxl import load_workbook

from .models import Category, Customer, Cart, CartProduct, Article, Collection, Feedback, Product, Series, \
    CDEKDeliveryPrice
from .models import Size, Purpose, Problem, TypeSkin, TypeHair, TypeProduct, Distributor, CDEKAuth, \
    Promocode, TypeOfDelivery, CDEKCities, CDEK_PVZ, RussianPostDelivery, Order
from .mixins import CartMixin
from .forms import LoginForm, RegistrationForm
from .forms import OrderAddressForm, OrderDeliveryForm
from .utils import recalc_cart

from .models import Category, Customer, Cart, CartProduct, Product
from .mixins import CartMixin
# from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_cart, reload_cdek, russian_mail_reload


# class MyQ(Q):
#     default = 'OR'


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'base.html', context)


class FilterProducts(DetailView):

    def get_size(self):
        return Size.objects.all()

    def get_face_problem(self):
        return Problem.objects.filter(category=2)

    def get_body_problem(self):
        return Problem.objects.filter(category=3)

    def get_hair_problem(self):
        return Problem.objects.filter(category=4)

    def get_purpose(self):
        return Purpose.objects.all()

    def get_typeskin(self):
        return TypeSkin.objects.all()

    def get_typeproduct(self):
        return TypeProduct.objects.all()

    def get_typehair(self):
        return TypeHair.objects.all()

    # Серии, разделены на категории. Модель одна, разняится поле "категория"

    def get_face_series(self):
        category = self.get_object()
        return Series.objects.filter(category=2)

    def get_body_series(self):
        category = self.get_object()
        return Series.objects.filter(category=3)

    def get_hair_series(self):
        category = self.get_object()
        return Series.objects.filter(category=4)


# class FilterProductsView(View):
#     filter_list = {}
#
#     def get(self, request, *args, **kwargs):
#         product_filter = request.GET
#         self.filter_list = product_filter.dict()
#         print(self.filter_list)
#         return render(request, 'category_detail.html')

class MainPageView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        articles = Article.objects.all()[:3]
        series = Series.objects.all()[:1]

        important_product = Product.objects.filter(is_important=True)[:4]
        context = {
            'categories': categories,
            'products': products,
            'important_product': important_product,
            'cart': self.cart,
            'articles': articles,
            'series': series,
        }
        return render(request, 'main_page.html', context)


class CategoryView(BaseView, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'choice_category.html', context)


class DeliveryCalculatorView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        self.query = request.GET
        context = {}
        if self.query:
            cities = RussianPostDelivery.objects.filter(city__contains=self.query.get('search_city').capitalize())
            context = {
                'cities': cities,
                'cart': self.cart
            }

        return render(request, 'delivery_calculator.html', context)


class ProductDetailView(CartMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_object().category.__class__.objects.all()
        context['cart'] = self.cart
        return context


# Комплексная хрень для отображения подробностей категорий, URL и slug категорий
class CategoryDetailView(CartMixin, FilterProducts):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'
    filter_list = {}

    # qty = int(request.POST.get('qty'))  # Получение с данных с формы по полю name
    # А вот какой формат данных получает - хз

    # ДАННАЯ ФУНКЦИЯ ВЫТАСКИВАЕТ ИНФОРМАЦИЮ О ТОМ, КАКАЯ СТРАНИЦА, ОБЪЕКТЫ И ПРОЧЕЕ СЕЙЧАС ПРОГРУЖЕНЫ
    def get_context_data(self, **kwargs, ):

        context = super().get_context_data(**kwargs)
        category = self.get_object()
        self.filter_list = self.request.GET

        # print(type(self.filter_list.values()))
        # self.filter_list_2 = {k: int(v) for k, v in self.filter_list.items()}
        # for value in self.filter_list.values():
        #     if type(value) == list:
        #         value = list(map(int, value))

        # print(self.filter_list)
        # final_category_products = category.product_set.filter(**self.filter_list)
        # print(final_category_products)
        #
        products = category.product_set.all()
        # context['category_products'] = final_category_products
        # Уход за волосами
        # Уход за кожей лица
        # Уход за кожей тела
        if category.title == 'Уход за кожей лица':
            if 'size' in self.filter_list:
                products = products.filter(size__in=self.filter_list.getlist('size')).distinct()
            if 'type_skin' in self.filter_list:
                products = products.filter(type_skin__in=self.filter_list.getlist('type_skin')).distinct()
            if 'problems' in self.filter_list:
                products = products.filter(problems__in=self.filter_list.getlist('problems')).distinct()
            if 'series' in self.filter_list:
                products = products.filter(series__in=self.filter_list.getlist('series')).distinct()

        if category.title == 'Уход за кожей тела':
            if 'size' in self.filter_list:
                products = products.filter(size__in=self.filter_list.getlist('size')).distinct()
            if 'purpose' in self.filter_list:
                products = products.filter(purpose__in=self.filter_list.getlist('purpose')).distinct()
            if 'typeproduct' in self.filter_list:
                products = products.filter(typeproduct__in=self.filter_list.getlist('typeproduct')).distinct()
            if 'series' in self.filter_list:
                products = products.filter(series__in=self.filter_list.getlist('series')).distinct()

        if category.title == 'Уход за волосами':
            if 'hair_type' in self.filter_list:
                products = products.filter(hair_type__in=self.filter_list.getlist('hair_type')).distinct()
            if 'problems' in self.filter_list:
                products = products.filter(problems__in=self.filter_list.getlist('problems')).distinct()
            if 'series' in self.filter_list:
                products = products.filter(series__in=self.filter_list.getlist('series')).distinct()

        context['category_products'] = products

        context['cart'] = self.cart
        context['categories'] = self.model.objects.all()
        print(self.filter_list)

        # Интересная конструкция как вернуть все продукты по данной категории

        # product_filter = request.GET
        # self.filter_list = product_filter.dict()
        # print(self.filter_list)

        # Для вывода критериев фильтра в шаблоне
        # print(self.filter_list)

        context['filter_typeskin'] = self.get_typeskin()
        context['filter_size'] = self.get_size()
        context['filter_face_problem'] = self.get_face_problem()
        context['filter_body_problem'] = self.get_body_problem()
        context['filter_hair_problem'] = self.get_hair_problem()
        context['filter_face_series'] = self.get_face_series()
        context['filter_body_series'] = self.get_body_series()
        context['filter_hair_series'] = self.get_hair_series()
        context['filter_purpose'] = self.get_purpose()
        context['filter_typeproduct'] = self.get_typeproduct()
        context['filter_typehair'] = self.get_typehair()

        category_products = category.product_set.all()  # product_set пушо ManyToMany

        final_products = category_products.filter()

        return context


class DistributorsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        distributors = Distributor.objects.all()
        query_len = distributors.count()
        distrib_1 = distributors[:query_len / 2]
        distrib_2 = distributors[query_len / 2:]
        context = {
            'distributors': distributors,
            'distrib_1': distrib_1,
            'distrib_2': distrib_2,
            'cart': self.cart
        }
        return render(request, 'distributors.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(cart=self.cart, product=product)
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен в корзину")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(cart=self.cart, product=product)

        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        print(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(cart=self.cart, product=product)

        qty = str(request.POST['changeQty'])  # Получение с данных с формы по полю name
        print(qty)
        if qty == '+':

            cart_product.qty += 1
        else:
            cart_product.qty -= 1

        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        return HttpResponseRedirect('/cart/')


class PromocodeActivateView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        code = request.GET.get('promocode')
        promocode = Promocode.objects.filter(code=code).first()

        if promocode:
            if promocode.active == False:
                messages.add_message(request, messages.INFO, "Промокод не активен")
                print('не активен')
                return HttpResponseRedirect('/cart/')

            if self.cart.active_promocode == True:
                messages.add_message(request, messages.INFO, "У Вас уже применен промокод")
                print('применен уже')
                return HttpResponseRedirect('/cart/')

            if promocode.type.title == 'Позиция в подарок':
                self.cart.products.all().order_by()
                messages.add_message(request, messages.INFO, 'Применен промокод: "Позиция в подарок"')

            if promocode.type.title == 'Скидка на позицию':
                sale_products_all = promocode.product.all().values('title')
                # sale_products_incard = []
                for product in sale_products_all:
                    self.cart.products.all().filter(product__title=product['title']).update(
                        multiplier=promocode.multiplier)
                    # sale_products_incard.append(product.title)
                for product in self.cart.products.all():
                    product.save()
                messages.add_message(request, messages.INFO,
                                     'Применен промокод: "Скидка на позицию"' + str(
                                         promocode.multiplier) + '%')

            if promocode.type.title == 'Бесплатная доставка':
                self.cart.free_delivery = True
                messages.add_message(request, messages.INFO, 'Применен промокод на бесплатную доставку')

            if promocode.type.title == 'Скидка на всю корзину':
                self.cart.products.all().update(multiplier=promocode.multiplier)
                discount = promocode.multiplier * 100
                for product in self.cart.products.all():
                    product.save()
                messages.add_message(request, messages.INFO, 'Применен промокод на скидку' + str(discount) + '%')

            # Сохраняем корзину и ценники
            self.cart.active_promocode = True
            self.cart.promocode = promocode
            self.cart.save()
            recalc_cart(self.cart)

        else:
            print('Такого промокода не найдено')
        return HttpResponseRedirect('/cart/')


class PromocodeDeactivateView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        for product in self.cart.products.all():
            product.multiplier = 1
            product.save()
        self.cart.active_promocode = False
        self.cart.promocode = None
        recalc_cart(self.cart)

        return HttpResponseRedirect('/cart/')


# ВЬЮШКА ДЛЯ ОТОБРАЖЕНИЯ КОРЗИНЫ
class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class DeliveryPaymentView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
        }
        return render(request, 'delivery_and_payment.html', context)


# Вьюшка для отображения выбора доставки
class GetDeliveryOrderView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            customer = Customer.objects.get(user=request.user)
            categories = Category.objects.all()
            order = Order.objects.filter(customer=customer).last()
            for delivery in order.available_delivery.all():
                print(delivery)
            context = {
                'cart': self.cart,
                'categories': categories,
                'order': order,
            }
            return render(request, 'order_delivery.html', context)
        else:
            return HttpResponseRedirect('/login/')

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.filter(customer=customer).last()

        delivery_code = request.POST['delivery_choice']
        pvz_code = request.POST['pvz_code']
        delivery_type = TypeOfDelivery.objects.get(code=delivery_code)

        if delivery_code == 'cdek':
            delivery_price = CDEKCities.objects.get(title=order.city).delivery_price
            cdek_pvz = CDEK_PVZ.objects.get(code=pvz_code)
        if delivery_code == 'russian-post':
            delivery_price = RussianPostDelivery.objects.get(region=order.region).delivery_price
        if delivery_code == 'courier':
            delivery_price = 300.00

        if pvz_code:
            Order.objects.filter(customer=customer, finished=False).update(selected_delivery=delivery_type,
                                                                           delivery_price=delivery_price,
                                                                           pvz_code=cdek_pvz)
        else:
            Order.objects.filter(customer=customer, finished=False).update(selected_delivery=delivery_type,
                                                                           delivery_price=delivery_price)

        return HttpResponseRedirect('/')


# Вьюшка для отображения формы заполнения адреса
class GetAddressOrderView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            form = OrderAddressForm(request.POST or None)
            context = {
                'cart': self.cart,
                'categories': categories,
                'form': form
            }
            return render(request, 'order_address.html', context)
        else:
            return HttpResponseRedirect('/login/')


class AddDeliveryOrderView(CartMixin, View):
    pass


# Обработчик формы для адреса и создания заказа
class CreateOrder(CartMixin, View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderAddressForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)  # Создаст объект, по модели, которая указана в форме в init
            # new_order.id = last_id + 1  # Нужно будет подредачить уникальный идентификатор, а то тут херня какая-то
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.mail = form.cleaned_data['mail']
            new_order.country = form.cleaned_data['country'].title()
            new_order.region = form.cleaned_data['region']
            city = form.cleaned_data['city'].split()

            if len(city) != 1:
                new_order.city = city[1]
            else:
                new_order.city = city[0]

            # new_order.city = form.cleaned_data['city'].split()[1]
            new_order.street = form.cleaned_data['street']
            new_order.building = form.cleaned_data['building']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()

            if CDEKCities.objects.filter(title=new_order.city):
                new_order.available_delivery.add(TypeOfDelivery.objects.get(code='cdek'))

            if new_order.city != 'Краснодар':
                new_order.available_delivery.add(TypeOfDelivery.objects.get(code='russian-post'))
            else:
                new_order.available_delivery.add(TypeOfDelivery.objects.get(code='courier'))

            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            # messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/order-delivery/')
        return HttpResponseRedirect('/')


# Обработчик, добавляет тип доставки


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        # print(request.session.session_key)
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        session_key = request.session.session_key
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )

            # Наша задача это разобраться с корзинами, а именно. Чтоб если Session Key одной корзины совпадает с
            # Session key другой корзины
            if user:
                login(request, user)
                # Нашли корзину пользователя по логину
                user_cart = Cart.objects.filter(owner=user.id)
                # Если корзина НЕ пуста, то...
                # Анонимной корзине даем нового хозяина, а старую корзину пользователя удаляем
                if self.cart.total_products != 0:
                    Cart.objects.filter(owner=user.id, in_order=False).delete()
                    Cart.objects.filter(session_key=session_key).update(owner=user.id, for_anonymous_user=False)

                return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {
            'form': form,
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'registration.html', context)


class ReloadCdekView(View):
    def get(self, request, *args, **kwargs):
        reload_cdek()
        return HttpResponseRedirect('/')
