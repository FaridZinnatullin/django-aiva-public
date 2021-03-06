# Generated by Django 3.2.7 on 2021-10-12 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Название статьи')),
                ('text', models.TextField(blank=True, verbose_name='Текст статьи')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата публикации статьи')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='Изображение')),
                ('video_url', models.TextField(null=True, verbose_name='Ссылка на видео')),
                ('time_to_read', models.TextField(null=True, verbose_name='Время на прочтение')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Общая цена')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
                ('active_promocode', models.BooleanField(default=False)),
                ('free_delivery', models.BooleanField(default=False)),
                ('session_key', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Имя категории')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('image_logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение миниатюра')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CDEK_PVZ',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20, verbose_name='Код ПВЗ')),
                ('title', models.CharField(max_length=50, verbose_name='Название ПВЗ')),
                ('longitude', models.FloatField(verbose_name='Долгота нас. пункта')),
                ('latitude', models.FloatField(verbose_name='Широта нас. пункта')),
                ('address', models.CharField(default='', max_length=255, verbose_name='Улица, дом, корпус и т.д')),
                ('address_full', models.CharField(default='', max_length=255, verbose_name='Полный адрес')),
                ('work_time', models.CharField(max_length=110, verbose_name='Режим работы')),
                ('type', models.CharField(max_length=20, verbose_name='Тип ПВЗ')),
                ('is_handout', models.BooleanField(verbose_name='Являчется пунктом выдачи')),
            ],
        ),
        migrations.CreateModel(
            name='CDEKAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=255, null=True, verbose_name='Идентификатор')),
                ('password', models.CharField(blank=True, max_length=255, null=True, verbose_name='Пароль')),
                ('token', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Токен')),
                ('token_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип токена')),
                ('edited_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
            ],
        ),
        migrations.CreateModel(
            name='CDEKCountry',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='Код СДЭК')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='CDEKDeliveryPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Страна')),
                ('region', models.CharField(blank=True, max_length=255, null=True, verbose_name='Регион')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Город')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='CDEKOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tariff_code', models.IntegerField(verbose_name='Код тарифа')),
                ('recipient_name', models.CharField(max_length=255, verbose_name='ФИО получателя')),
                ('recipient_phone', models.CharField(max_length=255, verbose_name='Номер телефона')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий к закау')),
                ('delivery_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_delivery_point', to='mainapp.cdek_pvz', verbose_name='Код ПВЗ получателя')),
                ('shipment_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_shipment_point', to='mainapp.cdek_pvz', verbose_name='Код ПВЗ отправителя')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Коллекция')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес')),
            ],
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=55, verbose_name='Город')),
                ('shop_name', models.CharField(blank=True, max_length=55, verbose_name='Название магазина')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на магазин (Если есть)')),
                ('url_inst', models.CharField(blank=True, max_length=255, null=True, verbose_name='Логин в инстаграмм БЕЗ СОБАЧКИ (Если есть)')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Краткое описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес магазина')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Описание')),
                ('category', models.ManyToManyField(blank=True, to='mainapp.Category', verbose_name='Проблема какой части тела')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('how_to_use', models.TextField(blank=True, null=True, verbose_name='Способ применения')),
                ('composition', models.TextField(blank=True, null=True, verbose_name='Состав')),
                ('recommendation', models.TextField(blank=True, null=True, verbose_name='Рекомендация')),
                ('storage_conditions', models.TextField(blank=True, null=True, verbose_name='Условия хранения')),
                ('container', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Тара/упаковка')),
                ('is_important', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
                ('collections', models.ManyToManyField(blank=True, related_name='related_products', to='mainapp.Collection')),
                ('problems', models.ManyToManyField(blank=True, to='mainapp.Problem', verbose_name='Проблема кожи лица (ТОЛЬКО ДЛЯ ЛИЦА)')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('mail', models.CharField(max_length=255, verbose_name='Почта')),
                ('purpose', models.CharField(max_length=255, verbose_name='Почта')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('diseases', models.TextField(max_length=1024, verbose_name='Заболевания')),
                ('type_of_skin', models.CharField(max_length=255, verbose_name='Тип кожи лица')),
                ('skin_condition', models.CharField(max_length=255, verbose_name='Состояние кожи')),
                ('skin_condition_other', models.TextField(max_length=1024, verbose_name='Дополнительное состояние кожи')),
                ('skin_problems', models.TextField(max_length=1024, verbose_name='Проблемы с кожей')),
                ('use_face_cosmetic', models.CharField(max_length=255, verbose_name='Какую косметику для лица ипользует')),
                ('other_cosmetic_description', models.TextField(max_length=1024, verbose_name='Описание используемой косметики')),
                ('other_cosmetic_danger', models.TextField(max_length=1024, verbose_name='Испльзует ли опасную косметику')),
                ('body_skin_condition', models.CharField(max_length=255, verbose_name='Состояние кожи тела')),
                ('body_skin_problems', models.TextField(max_length=1024, verbose_name='Дополнительные проблемы кожи тела')),
                ('use_body_cosmetic', models.TextField(max_length=255, verbose_name='Какую косметику для тела ипользует')),
                ('test', models.TextField(max_length=23)),
            ],
        ),
        migrations.CreateModel(
            name='RussianPostDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255, verbose_name='Регион')),
                ('district', models.CharField(max_length=255, verbose_name='Округ')),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена доставки ПР')),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Тип доставки')),
                ('code', models.CharField(max_length=55, verbose_name='Код')),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfPromocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Тип промокода')),
            ],
        ),
        migrations.CreateModel(
            name='TypeSkin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Описание')),
                ('category', models.ManyToManyField(blank=True, to='mainapp.Category', verbose_name='Проблема какой части тела')),
            ],
        ),
        migrations.CreateModel(
            name='TypeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Описание')),
                ('category', models.ManyToManyField(blank=True, to='mainapp.Category', verbose_name='Проблема какой части тела')),
            ],
        ),
        migrations.CreateModel(
            name='TypeHair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Описание')),
                ('category', models.ManyToManyField(blank=True, to='mainapp.Category', verbose_name='Проблема какой части тела')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Описание')),
                ('category', models.ManyToManyField(blank=True, to='mainapp.Category', verbose_name='Проблема какой части тела')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
                ('products', models.ManyToManyField(blank=True, related_name='related_series', to='mainapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Описание')),
                ('category', models.ManyToManyField(blank=True, to='mainapp.Category', verbose_name='Проблема какой части тела')),
            ],
        ),
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='Промокод')),
                ('active', models.BooleanField(default=False, verbose_name='Активен')),
                ('created_at', models.DateField(auto_now=True, null=True, verbose_name='Дата создания промокода')),
                ('multiplier', models.FloatField(blank=True, null=True, verbose_name='Множитель скидки')),
                ('product', models.ManyToManyField(blank=True, to='mainapp.Product', verbose_name='На какой продукт скидка')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.typeofpromocode', verbose_name='Тип промокода')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='purpose',
            field=models.ManyToManyField(blank=True, to='mainapp.Purpose', verbose_name='Назначение (ТОЛЬКО ДЛЯ ТЕЛА)'),
        ),
        migrations.AddField(
            model_name='product',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='mainapp.series'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, to='mainapp.Size', verbose_name='Объем/вес'),
        ),
        migrations.AddField(
            model_name='product',
            name='type_hair',
            field=models.ManyToManyField(blank=True, to='mainapp.TypeHair', verbose_name='Тип волос (ТОЛЬКО ДЛЯ ВОЛОС)'),
        ),
        migrations.AddField(
            model_name='product',
            name='type_product',
            field=models.ManyToManyField(blank=True, to='mainapp.TypeProduct', verbose_name='Тип продукта (ТОЛЬКО ДЛЯ ТЕЛА)'),
        ),
        migrations.AddField(
            model_name='product',
            name='type_skin',
            field=models.ManyToManyField(blank=True, to='mainapp.TypeSkin', verbose_name='Тип кожи (ТОЛЬКО ДЛЯ ЛИЦА)'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Стоимость доставки')),
                ('mail', models.CharField(max_length=255, verbose_name='Почта')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('country', models.CharField(max_length=255, verbose_name='Страна')),
                ('region', models.CharField(max_length=255, verbose_name='Регион/Край')),
                ('city', models.CharField(max_length=255, verbose_name='Город/Населенный пункт')),
                ('street', models.CharField(max_length=255, verbose_name='Улица')),
                ('building', models.CharField(max_length=255, verbose_name='Дом, корпус, квартира...')),
                ('index', models.CharField(blank=True, max_length=255, null=True, verbose_name='Индекс-хуиндекс')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('finished', models.BooleanField(default=False)),
                ('available_delivery', models.ManyToManyField(blank=True, null=True, related_name='related_order', to='mainapp.TypeOfDelivery', verbose_name='Возможные варианты доставки')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cart', verbose_name='Корзина')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to='mainapp.customer', verbose_name='Покупатель')),
                ('delivery_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekorder', verbose_name='Заказ в СДЭКе')),
                ('pvz_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdek_pvz', verbose_name='Заказ в СДЭКе')),
                ('selected_delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.typeofdelivery', verbose_name='Выбранный тип доставки')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата публикации отзыва')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer', verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(related_name='related_order', to='mainapp.Order', verbose_name='Заказы покупателя'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='collection',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_collection', to='mainapp.Product'),
        ),
        migrations.CreateModel(
            name='CDEKRegions',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False, verbose_name='Код СДЭК')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('country', models.ForeignKey(blank=True, max_length=5, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekcountry', verbose_name='Страна')),
            ],
        ),
        migrations.CreateModel(
            name='CDEKCities',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Код СДЭК')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота нас. пункта')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Широта нас. пункта')),
                ('cdek', models.BooleanField(default=False, verbose_name='Наличие пунктов СДЭК')),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=9, null=True, verbose_name='Стоимость доставки')),
                ('delivery_period_min', models.IntegerField(null=True, verbose_name='Минимальный срок доставки')),
                ('delivery_period_max', models.IntegerField(null=True, verbose_name='Максимальный срок доставки')),
                ('country', models.ForeignKey(blank=True, max_length=5, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekcountry', verbose_name='Страна')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekregions', verbose_name='Регион')),
            ],
        ),
        migrations.AddField(
            model_name='cdek_pvz',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekcities', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='cdek_pvz',
            name='country',
            field=models.ForeignKey(blank=True, max_length=5, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekcountry', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='cdek_pvz',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cdekregions', verbose_name='Регион'),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=9, verbose_name='Коеффициент цены')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Итоговая цена продукта')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='mainapp.cart', verbose_name='Корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Продукт')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer', verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='related_cart', to='mainapp.CartProduct'),
        ),
        migrations.AddField(
            model_name='cart',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.promocode', verbose_name='Примененный промокод'),
        ),
    ]
