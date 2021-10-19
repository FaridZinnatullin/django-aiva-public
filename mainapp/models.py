from django.db import models
from django.contrib.auth import get_user_model

from django.urls import reverse
from django.utils import timezone

#Результат этой функции выдает нам, который прописан в settings

User = get_user_model()




# КАТЕГОРИИ ПРОДУКТОВ
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Имя категории')
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    image_logo = models.ImageField(verbose_name='Изображение миниатюра', null=True, blank=True)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Напомню, reverse нужен для генерации URL'ов. Оно уже было описано чуть ранее
        return reverse('category_detail', kwargs={'slug': self.slug})

# Одна общая модель для всех продуктов
class Product(models.Model):

    # Основные поля. Общие для всех категорий
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)
    series = models.ForeignKey('Series', related_name='related_products', null=True, blank=True, on_delete=models.CASCADE)
    collections = models.ManyToManyField('Collection', related_name='related_products', blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)

    how_to_use = models.TextField(verbose_name='Способ применения', null=True, blank=True)
    composition = models.TextField(verbose_name='Состав', null=True, blank=True)
    recommendation = models.TextField(verbose_name='Рекомендация', null=True, blank=True)
    storage_conditions = models.TextField(verbose_name='Условия хранения', null=True, blank=True)
    container = models.TextField(max_length=1024, verbose_name='Тара/упаковка', null=True, blank=True)

    is_important = models.BooleanField(default=False)

    # Необязательные поля для фильтров. Могут быть пустыми

    size = models.ManyToManyField('Size', verbose_name='Объем/вес', blank=True)
    problems = models.ManyToManyField('Problem', verbose_name='Проблема кожи лица (ТОЛЬКО ДЛЯ ЛИЦА)', blank=True)
    type_skin = models.ManyToManyField('TypeSkin', verbose_name='Тип кожи (ТОЛЬКО ДЛЯ ЛИЦА)', blank=True)
    purpose = models.ManyToManyField('Purpose', verbose_name='Назначение (ТОЛЬКО ДЛЯ ТЕЛА)', blank=True)
    type_product = models.ManyToManyField('TypeProduct', verbose_name='Тип продукта (ТОЛЬКО ДЛЯ ТЕЛА)', blank=True)
    type_hair = models.ManyToManyField('TypeHair', verbose_name='Тип волос (ТОЛЬКО ДЛЯ ВОЛОС)', blank=True)



    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_model_name(self):
        return self.__class__.__name__.lower()

class RussianPostDelivery(models.Model):
    region = models.CharField(max_length=255, verbose_name='Регион')
    district = models.CharField(max_length=255, verbose_name='Округ')
    delivery_price = models.DecimalField(verbose_name='Цена доставки ПР', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.region

class Series(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название')
    products = models.ManyToManyField(Product, related_name='related_series', blank=True)
    description = models.TextField(max_length=1024, verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True)


    def __str__(self):
        return self.title



# ДЛЯ ТОГО, ЧТОБ СОЗДАТЬ CARTPRODUCT МОЖНО ВОСПОЛЬЗОВАТЬСЯ СЛЕДУЮЩЕЙ КОНСТРУКЦИЕЙ:
# notebook = Notebook.objects.create(.....) СОЗДАСТ ОБЪЕКТ КЛАССА Notebook и запишет его в переменную notebook
# notebook = Notebook.objects.first(.....) ВЕРНЕТ ПЕРВЫЙ ОБЪЕКТ ИЗ БД КЛАССА Notebook
# customer = Customer.objects.create(...) СОЗДАСТ ОБЪЕКТ КЛАССА Customer и запишет его в переменную customer
# cart = Cart.objects.create(...) СОЗДАСТ ОБЪЕКТ КЛАССА Cart и запишет его в переменную cart
# cp = CartProduct.objects.create(content_object = notebook, user = customer, cart = cart)
# cart.products.add(cp) - Добавление cp (объект CartProduct) в корзину cart (объект Cart);
# products - поле у объекта Cart

class CartProduct(models.Model):

    # ПОЛЬЗОВАТЕЛЬ, КОТОРОМУ ПРИНАДЛЕЖИТ ЭТОТ ТОВАР (В ЧЬЕЙ КОРЗИНЕ ЛЕЖИТ ТОВАР)
    # CUSTOMER В КАВЫЧКАХ ПОТОМУ ЧТО МОДЕЛЬ ЕЩЕ НЕ ОБЪЯВИЛИ
    #user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)

    # КОРЗИНА, КОТОРОЙ ПРИНАДЛЕЖИТ ЭТОТ ТОВАР ( В КАКОЙ ИМЕННО КОРЗИНЕ ЛЕЖИТ)
    # CART В КАВЫЧКАХ ПОТОМУ ЧТО МОДЕЛЬ ЕЩЕ НЕ ОБЪЯВИЛИ
    # В related_name нужно написать как именно называется связь если два ФК ссылаются друг на друга
    # Здесь related_name означает, что это СВЯЗАННЫЕ С КОРЗИНОЙ ПРОДУКТЫ. Писать можно что угодно
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')

    product = models.ForeignKey(Product, verbose_name='Продукт', null = False, on_delete=models.CASCADE)
    multiplier = models.DecimalField(max_digits= 9, decimal_places=2, verbose_name='Коеффициент цены', default=1)

    #==========================================================
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField( max_digits= 9, decimal_places=2, verbose_name='Итоговая цена продукта')

    # Конструкция типа «return “Покупатель: {}{}.format(self.user.first_name, self.user.last_name)» –
    # в пустые фигурные скобки засунет значения их переменных в скобках.Например: Покупатель: ИванИванов
    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price * self.multiplier
        super().save(*args, **kwargs)

    # def sale(self, *args, **kwargs):
    #     self.final_price = self.final_price * coeff
    #     super().save(*args, **kwargs)

class Cart(models.Model):
    # ПОЛЬЗОВАТЕЛЬ - ВЛАДЕЛЕЦ ОПРЕДЕЛЕННОЙ КОРЗИНЫ
    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)

    # ПРОДУКТЫ - ПРОДУКТЫ, ИМЕЮЩИЕСЯ В ДАННОЙ КОРЗИНЕ. СВЯЗЬ МНОГИЕ КО МНОГИМ, ПОТОМУ ЧТО ПРОДУКТОВ В КОРЗИНЕ МНОГО
    # BLANK = TRUE - ЕСЛИ НЕТ ЗНАЧЕНИЯ, БУДЕТ ПУСТАЯ СТРОКА, А НЕ NULL
    # В related_name нужно написать как именно называется связь если два ФК ссылаются друг на друга
    # Здесь related_name означает, что это СВЯЗАННАЯ С ПРОДУКТАМИ КОРЗИНА. Писать можно что угодно
    products = models.ManyToManyField(CartProduct, related_name='related_cart')

    # Допустим, есть некий cartproduct (инстанс его) и мы хотим узнать К КАКОЙ КОРЗИНЕ ОН ОТНОСИТСЯ, то пишем следующее:
    # cartproduct.related_cart.all()

    # Допустим, есть некая корзина cart (инстанс её) и мы хотим узнать КАКИЕ ПРОДУКТЫ В НЕЙ ЕСТЬ, то пишем следующее:
    # cart.related_product.all()

    # ПО ДЕФОЛТУ 0 ЧТОБ ПОКАЗЫВАТЬ КОРРЕКТНОЕ КОЛИЧЕСТВО ТОВАРОВ В КОРЗИНЕ ЕСЛИ ОНА ПУСТАЯ
    # СОДЕРЖИТ КОЛИЧЕСТВО РАЗНЫХ ПРОДУКТОВ В КОРЗИНЕ. БЕЗ ПОВТОРОВ
    total_products = models.PositiveIntegerField(default=0)

    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')

    in_order = models.BooleanField(default=False)


    for_anonymous_user = models.BooleanField(default=False)

    promocode = models.ForeignKey('Promocode', verbose_name='Примененный промокод', blank=True, null=True, on_delete=models.CASCADE)

    active_promocode = models.BooleanField(default=False)

    free_delivery = models.BooleanField(default=False)


    session_key = models.CharField(max_length=32, null=True)

    # ОТОБРАЖАТЬ БУДЕМ ИМЕННО ID КОРЗИНЫ ДЛЯ УДОБСТВА (Имени то у нее нет)
    def __str__(self):
        return str(self.id)

class Article(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название статьи', blank=True)
    text = models.TextField(verbose_name='Текст статьи', blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата публикации статьи')
    image = models.ImageField(verbose_name='Изображение', null=True)
    video_url = models.TextField(verbose_name='Ссылка на видео', null=True)
    time_to_read = models.TextField(verbose_name='Время на прочтение', null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title





class Collection(models.Model):

    title = models.CharField(max_length=255, verbose_name='Коллекция', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='related_collection', blank=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    # User - ИМЕЕТСЯ В ВИДУ МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ ИЗ СТАНДАРТНОГО ДЖАНГО. ОНА КАК ОСНОВА
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    # Конструкция типа «return “Покупатель: {}{}.format(self.user.first_name, self.user.last_name)» –
    # в пустые фигурные скобки засунет значения их переменных в скобках.Например: Покупатель: ИванИванов
    # first_name, last_name, email берем из стандартной модели User

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

class Feedback(models.Model):

    user = models.ForeignKey(Customer, verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата публикации отзыва')
    def __str__(self):
        return str(self.id)

class Distributor(models.Model):

    city = models.CharField(max_length=55, verbose_name='Город', blank=True)
    shop_name = models.CharField(max_length=55, verbose_name='Название магазина', blank=True)
    url = models.CharField(max_length=255, verbose_name='Ссылка на магазин (Если есть)', null=True, blank=True)
    url_inst = models.CharField(max_length=255, verbose_name='Логин в инстаграмм БЕЗ СОБАЧКИ (Если есть)', null=True, blank=True)
    description = models.TextField(verbose_name='Краткое описание', null=True, blank=True)
    image = models.ImageField(verbose_name='Фото', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес магазина', null=True, blank=True)

    def __str__(self):
        return str(self.shop_name)

class TypeOfDelivery(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тип доставки', blank=True)
    code = models.CharField(max_length=55, verbose_name='Код')
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

# class Delivery(models.Model):
#     delivery = models.ForeignKey(TypeOfDelivery, verbose_name='Тип доставки', null=True, blank=True)
#     price = models.IntegerField()
#
#     def __str__(self):
#         return str(self.delivery)

class Order(models.Model):

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)

    available_delivery = models.ManyToManyField(TypeOfDelivery, verbose_name='Возможные варианты доставки', related_name='related_order', null=True, blank=True)
    selected_delivery = models.ForeignKey(TypeOfDelivery, verbose_name='Выбранный тип доставки', on_delete=models.CASCADE, null=True, blank=True)
    delivery_price = models.DecimalField(verbose_name='Стоимость доставки', max_digits=9, decimal_places=2, null=True, blank=True)

    pvz_code = models.ForeignKey('CDEK_PVZ', verbose_name='Код ПВЗ СДЭКа', on_delete=models.CASCADE, null=True, blank=True)
    delivery_order = models.ForeignKey('CDEKOrder', verbose_name='Заказ в СДЭКе', on_delete=models.CASCADE, null=True, blank=True)


    mail = models.CharField(verbose_name='Почта', max_length=255)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    country = models.CharField(max_length=255, verbose_name='Страна')
    region = models.CharField(max_length=255, verbose_name='Регион/Край')
    city = models.CharField(max_length=255, verbose_name='Город/Населенный пункт')
    street = models.CharField(max_length=255, verbose_name='Улица')
    building = models.CharField(max_length=255, verbose_name='Дом, корпус, квартира...')
    index = models.CharField(max_length=255, verbose_name='Индекс-хуиндекс', null=True, blank=True)

    phone = models.CharField(max_length=20, verbose_name='Телефон')
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    # created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    finished = models.BooleanField(default=False, null=False)

    def __str__(self):
        return str(self.id)

class Questionnaire(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=255)
    mail = models.CharField(verbose_name='Почта', max_length=255)
    purpose = models.CharField(verbose_name='Почта', max_length=255)
    age = models.IntegerField(verbose_name='Возраст')
    diseases = models.TextField(verbose_name= 'Заболевания', max_length=1024)
    type_of_skin = models.CharField(verbose_name='Тип кожи лица', max_length=255)
    skin_condition = models.CharField(verbose_name='Состояние кожи', max_length=255)
    skin_condition_other = models.TextField(verbose_name='Дополнительное состояние кожи', max_length=1024)
    skin_problems = models.TextField(verbose_name='Проблемы с кожей', max_length=1024)
    use_face_cosmetic = models.CharField(verbose_name='Какую косметику для лица ипользует', max_length=255)
    other_cosmetic_description = models.TextField(verbose_name='Описание используемой косметики', max_length=1024)
    other_cosmetic_danger = models.TextField(verbose_name='Испльзует ли опасную косметику', max_length=1024)
    body_skin_condition = models.CharField(verbose_name= 'Состояние кожи тела', max_length=255)
    body_skin_problems = models.TextField(verbose_name='Дополнительные проблемы кожи тела', max_length=1024)
    use_body_cosmetic = models.TextField(verbose_name='Какую косметику для тела ипользует', max_length=255)
    test = models.TextField(max_length=23)

    def __str__(self):
        return str(self.name)


class CDEKAuth(models.Model):
    user =  models.CharField(verbose_name='Идентификатор', max_length=255, null=True, blank=True)
    password = models.CharField(verbose_name='Пароль', max_length=255, null=True, blank=True)
    token = models.TextField(verbose_name='Токен', max_length=2048, null=True, blank=True)
    token_type = models.CharField(verbose_name='Тип токена', max_length=255, null=True, blank=True)
    # edited_at = models.DateField(verbose_name='Дата последнего обновления', default=timezone.now)
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class CDEKDeliveryPrice(models.Model):
    country = models.CharField(verbose_name='Страна', max_length=255, null=True, blank=True)
    region = models.CharField(verbose_name='Регион', max_length=255, null=True, blank=True)
    city = models.CharField(verbose_name='Город', max_length=255, null=True, blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return "Страна: {}; Регион: {}; Город: {}; Цена: {};".format(self.country, self.region, self.city, self.price)




class CDEK_PVZ(models.Model):

    id = models.AutoField(primary_key=True)
    code = models.CharField(verbose_name='Код ПВЗ', max_length=20)
    title = models.CharField(verbose_name='Название ПВЗ', max_length=50)

    country = models.ForeignKey('CDEKCountry', verbose_name='Страна', max_length=5, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey('CDEKRegions', verbose_name='Регион', on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey('CDEKCities', verbose_name='Город', on_delete=models.CASCADE, null=True, blank=True)


    longitude = models.FloatField(verbose_name='Долгота нас. пункта')
    latitude = models.FloatField(verbose_name='Широта нас. пункта')

    address = models.CharField(verbose_name='Улица, дом, корпус и т.д', max_length=255, default='')
    address_full = models.CharField(verbose_name='Полный адрес', max_length=255, default='')


    work_time = models.CharField(verbose_name='Режим работы', max_length = 110)

    type = models.CharField(verbose_name='Тип ПВЗ', max_length=20)

    is_handout = models.BooleanField(verbose_name='Являчется пунктом выдачи')





    def __str__(self):
        return self.code

    # URL https://api.cdek.ru/v2/deliverypoints



class CDEKCities(models.Model):

    code = models.CharField(verbose_name='Код СДЭК', max_length=20,  primary_key=True)
    title = models.CharField(verbose_name='Название', max_length=255)

    country = models.ForeignKey('CDEKCountry', verbose_name='Страна', max_length=5, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey('CDEKRegions', verbose_name='Регион', on_delete=models.CASCADE, null=True, blank=True)

    longitude = models.FloatField(verbose_name='Долгота нас. пункта', null=True, blank=True)
    latitude = models.FloatField(verbose_name='Широта нас. пункта', null=True, blank=True)
    cdek = models.BooleanField(verbose_name='Наличие пунктов СДЭК', default=False)

    delivery_price = models.DecimalField(verbose_name='Стоимость доставки', max_digits=9, decimal_places=2, null=True)

    delivery_period_min = models.IntegerField(verbose_name='Минимальный срок доставки', null=True)
    delivery_period_max = models.IntegerField(verbose_name='Максимальный срок доставки', null=True)


    def __str__(self):
        return self.title
    # # URL https://api.cdek.ru/v2/location/cities


class CDEKRegions(models.Model):
    code = models.IntegerField(verbose_name='Код СДЭК', primary_key=True)
    title = models.CharField(verbose_name='Название', max_length=255)
    country = models.ForeignKey('CDEKCountry', verbose_name='Страна', max_length=5, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    # URL 	https://api.cdek.ru/v2/location/regions

class CDEKCountry(models.Model):
    code = models.CharField(verbose_name='Код СДЭК', max_length=5, primary_key=True)
    title = models.CharField(verbose_name='Название', max_length=255)

    def __str__(self):
        return self.title




class CDEKOrder(models.Model):
    tariff_code = models.IntegerField(verbose_name='Код тарифа')
    shipment_point = models.ForeignKey(CDEK_PVZ, related_name='related_shipment_point', verbose_name='Код ПВЗ отправителя', on_delete=models.CASCADE, null= True, blank= True)
    delivery_point = models.ForeignKey(CDEK_PVZ, related_name='related_delivery_point', verbose_name='Код ПВЗ получателя', on_delete=models.CASCADE, null= True, blank= True)
    recipient_name = models.CharField(verbose_name='ФИО получателя', max_length=255)
    recipient_phone = models.CharField(verbose_name='Номер телефона', max_length=255)
    comment = models.CharField(verbose_name='Комментарий к закау', max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.recipient_name)




class Promocode(models.Model):
    code = models.CharField(verbose_name='Промокод', max_length=255)
    type = models.ForeignKey('TypeOfPromocode', verbose_name='Тип промокода',  null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name='Активен', default=False)
    created_at = models.DateField(verbose_name='Дата создания промокода',  null=True, blank=True, auto_now=True)
    multiplier = models.FloatField(verbose_name='Множитель скидки', null=True, blank=True)
    product = models.ManyToManyField(Product, verbose_name='На какой продукт скидка', blank=True)

    def __str__(self):
        return "Промокод: {}; Тип промокода: {};".format(self.code, self.type)






class TypeOfPromocode(models.Model):
    title = models.CharField(verbose_name='Тип промокода', max_length=255)

    def __str__(self):
        return "Тип промокода: {};".format(self.title)


# Общие фильтры-----------------------------------------------------------------
class Size(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', max_length=255, null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Проблема какой части тела', blank=True)

    def __str__(self):
        return self.title


class Problem(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', max_length=255, null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Проблема какой части тела', blank=True)

    def __str__(self):
        return self.title



# Фильтры для лица---------------------------------------------------------------
class TypeSkin(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', max_length=255, null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Проблема какой части тела', blank=True)

    def __str__(self):
        return self.title

# Фильтры для тела---------------------------------------------------------------

class Purpose(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', max_length=255, null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Проблема какой части тела', blank=True)

    def __str__(self):
        return self.title

class TypeProduct(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', max_length=255, null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Проблема какой части тела', blank=True)

    def __str__(self):
        return self.title


# Фильтры для волос-----------------------------------------------------------

class TypeHair(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', max_length=255, null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Проблема какой части тела', blank=True)

    def __str__(self):
        return self.title







