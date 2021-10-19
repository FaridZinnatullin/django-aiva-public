import json
import requests
import datetime
import time
from django.db import models
from .models import CDEK_PVZ, CDEKRegions, CDEKCities, CDEKAuth, CDEKCountry, RussianPostDelivery


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()


def update_key():
    # if not CDEKAuth.objects.all().exists():
    #     ID = '#'
    #     Pass = '#'
    #     response = requests.post(
    #         f"https://api.cdek.ru/v2/oauth/token?client_id={ID}&client_secret={Pass}&grant_type=client_credentials")
    #     response = response.json()
    #     CDEKAuth.objects.create(
    #         user=ID,
    #         password=Pass,
    #         token=response['access_token']
    #     )
    #

    # Обновлялка токена

    key = CDEKAuth.objects.first()
    old_time = key.edited_at
    now_time = datetime.datetime.now()

    if now_time.hour != old_time.hour:
        response = requests.post(
            f"https://api.cdek.ru/v2/oauth/token?client_id={key.user}&client_secret={key.password}&grant_type=client_credentials")
        response = response.json()
        CDEKAuth.objects.filter(id=2).update(edited_at=now_time, token=response['access_token'])



def reload_cdek():
    try:
        CDEKCountry.objects.all().delete()
        CDEKRegions.objects.all().delete()
        CDEKCities.objects.all().delete()
        CDEK_PVZ.objects.all().delete()
    except:
        print('Any error with BD')

    # Вытаскиваем ключ из БД
    update_key()
    key = CDEKAuth.objects.first()

    # Создание стран
    CDEKCountry.objects.create(code='RU', title='Россия')
    CDEKCountry.objects.create(code='BY', title='Белоруссия (Беларусь)')
    CDEKCountry.objects.create(code='KZ', title='Казахстан')
    CDEKCountry.objects.create(code='UA', title='Украина')

    # Создание регионов
    regions = requests.get(
        'https://api.cdek.ru/v2/location/regions?country_codes=RU,KZ,UA,BY',
        params={},
        headers={'Authorization': f"Bearer {key.token}", 'Content-Type': 'application/json'}
    )

    regions = regions.json()

    for region in regions:
        CDEKRegions.objects.create(
            code=region['region_code'],
            title=region['region'],
            country=CDEKCountry.objects.filter(code=region['country_code']).first(),
        )

    # Создание городов
    cities = requests.get(
        'https://api.cdek.ru/v2/location/cities?size=100000&country_codes=RU,KZ,UA,BY',
        params={},
        headers={'Authorization': f"Bearer {key.token}", 'Content-Type': 'application/json'}
    )

    cities = cities.json()

    for city in cities:
        try:
            CDEKCities.objects.create(
                code=city['code'],
                title=city['city'],
                country=CDEKCountry.objects.filter(code=city['country_code']).first(),
                region=CDEKRegions.objects.filter(code=city['region_code']).first(),

                longitude=city['longitude'],
                latitude=city['latitude'],
            )
        except KeyError:
            print('Вылет города: ' + city['city'])

    # Создание ПВЗ
    pvz_ru = requests.get(
        'https://api.cdek.ru/v2/deliverypoints?country_code=RU',
        params={},
        headers={'Authorization': f"Bearer {key.token}", 'Content-Type': 'application/json'}
    )
    pvz_ru = pvz_ru.json()

    pvz_kz = requests.get(
        'https://api.cdek.ru/v2/deliverypoints?country_code=KZ',
        params={},
        headers={'Authorization': f"Bearer {key.token}", 'Content-Type': 'application/json'}
    )
    pvz_kz = pvz_kz.json()

    pvz_by = requests.get(
        'https://api.cdek.ru/v2/deliverypoints?country_code=BY',
        params={},
        headers={'Authorization': f"Bearer {key.token}", 'Content-Type': 'application/json'}
    )
    pvz_by = pvz_by.json()

    pvz_ua = requests.get(
        'https://api.cdek.ru/v2/deliverypoints?country_code=UA',
        params={},
        headers={'Authorization': f"Bearer {key.token}", 'Content-Type': 'application/json'}
    )
    pvz_ua = pvz_ua.json()

    pvz = [pvz_ru, pvz_kz, pvz_by, pvz_ua]
    for country in pvz:
        for point in country:
            try:
                CDEK_PVZ.objects.create(
                    code=point['code'],
                    title=point['name'],

                    country=CDEKCountry.objects.filter(code=point['location']['country_code']).first(),
                    region=CDEKRegions.objects.filter(code=point['location']['region_code']).first(),
                    city=CDEKCities.objects.filter(code=point['location']['city_code']).first(),

                    longitude=point['location']['longitude'],
                    latitude=point['location']['latitude'],

                    address=point['location']['address'],
                    address_full=point['location']['address_full'],

                    work_time=point['work_time'],

                    type=point['type'],

                    is_handout=point['is_handout']

                )
            except:
                print(point['code'])

    # Находим те города, в которых есть СДЭК, ставим метку
    cities = CDEKCities.objects.all()
    for city in cities:
        if CDEK_PVZ.objects.filter(city=city):
            CDEKCities.objects.filter(code=city.code).update(cdek=True)

    # Удаляем города без СДЕКа
    CDEKCities.objects.filter(cdek=False).delete()



    # Устанавливаем цены на доставку
    cities = CDEKCities.objects.all()
    for city in cities:
        info = get_info(city.title)

        if CDEK_PVZ.objects.filter(city=city):
            print(f"Обновляется для города: ${city.title}")
            CDEKCities.objects.filter(code=city.code).update(delivery_price=info['price'],
                                                             delivery_period_min=info['period_min'],
                                                             delivery_period_max=info['period_max'])


# Информация о стоимости и сроках доставки в определенный город
def get_info(city):
    time.sleep(2)
    update_key()
    key = CDEKAuth.objects.first()

    city_from = CDEKCities.objects.filter(title='Краснодар').first().code,
    city_to = CDEKCities.objects.filter(title=city).first().code,

    city_to = int(city_to[0])
    city_from = int(city_from[0])

    query = {
        "type": 1,
        "from_location": {
            "code": city_from
        },
        "to_location": {
            "code": city_to
        },

        "packages": [
            {
                "height": 20,
                "length": 6,
                "weight": 2000,
                "width": 20
            }
        ]
    }

    query_json = json.dumps(query)

    prices = requests.post(
        url="https://api.cdek.ru/v2/calculator/tarifflist",
        params={},
        data=query_json,
        headers={'Authorization': f"Bearer {key.token}", 'Content-Type': 'application/json'}
    )

    prices = prices.json()
    price = 0
    period_max = 0
    period_min = 0
    first_priority = [234, 378]
    second_priority = [136, 368]

    # Тарифы: 234 (эко с-с), 378 (эко с-п) 136 (с-с), 368(с-п)
    for tariff in prices['tariff_codes']:
        if 'tariff_code' in tariff:
            if tariff['tariff_code'] in first_priority:
                price = tariff['delivery_sum']
                period_min = tariff['period_min']
                period_max = tariff['period_max']
                print(f'Сработал тариф эконом для города')
                break

            if tariff['tariff_code'] in second_priority:
                price = tariff['delivery_sum']
                period_min = tariff['period_min']
                period_max = tariff['period_max']

    info = {
        'price': price,
        'period_min': period_min,
        'period_max': period_max,
    }
    return info


def russian_mail_reload():
    regions = RussianPostDelivery.objects.all()
    for region in regions:
        title = region.region.split()

        if len(title) == 2:
            if 'край' in title:
                title.reverse()
                RussianPostDelivery.objects.filter(id=region.id).update(region=" ".join(title))
            if 'область' in title:
                title.reverse()
                title[0] = 'обл'
                RussianPostDelivery.objects.filter(id=region.id).update(region=" ".join(title))
