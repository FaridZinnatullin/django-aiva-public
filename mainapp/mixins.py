from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View

from .models import Category, Cart, Customer, Product


# "Mixin это класс, у которого есть определенный функционал, но он бесполезен без применения его к главному классу"
# По сути эти миксины мы используем только для того, чтоб корректно отображать список категорий и корзину везде, но зачем...
# Гемора выше крыши. Проще сделать HTML шаблон для категорий и инклудить его


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.save()
        self.session = request.session

        # Если пользователь авторизирован, то
        if request.user.is_authenticated:
            # Ищем пользователя в нашей БД
            customer = Customer.objects.filter(user=request.user).first()
            # Если не найден, то
            if not customer:
                # Создаем нового пользователя
                customer = Customer.objects.create(user=request.user)

            # Далее ищем корзину данного пользователя
            cart = Cart.objects.filter(owner=customer, in_order=False).first()

            # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ЗАЛОГИНИЛСЯ ВПЕРВЫЕ И НЕ ИМЕЕТ КОРЗИНЫ
            # Если корзина не найдена, то создаем и присваиваем ей сессионный ключ
            if not cart:
                cart = Cart.objects.create(owner=customer, session_key=request.session.session_key)
                cart.session_key = request.session.session_key
                print('Создали НЕанонимную корзину c ID: ' + str(cart.id))
                print('Сессионный номер корзины: ' + str(cart.session_key))


        # Если пользователь не авторизирован, то
        else:

            # Ищем корзину по сессионному ключу
            cart = Cart.objects.filter(session_key=request.session.session_key, for_anonymous_user=True).first()
            print(request.session.session_key)
            # Если таковой корзина не найдена, то..
            if not cart:
                # То создаем корзину
                session_key = request.session.session_key
                print(session_key)
                cart = Cart.objects.create(session_key=request.session.session_key, for_anonymous_user=True)
                print('Создали анонимную корзину c ID: ' + str(cart.id))
                print('Сессионный номер корзины: ' + str(cart.session_key))

        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
