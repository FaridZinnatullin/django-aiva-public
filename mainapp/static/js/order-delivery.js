function setpvz(address, code){
    $('#select-pvz').html(`Выбран пункт выдачи по адресу: ${address}`);
    $('#id_pvz').val(String(code));

}
function init(city_info) {
    var coordinates = []

    coordinates = [city_info.latitude, city_info.longitude];

    cdekPrice = city_info.delivery_price
    var myMap = new ymaps.Map('map', {
            center: coordinates,
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        }),

        objectManager = new ymaps.ObjectManager({
            // Чтобы метки начали кластеризоваться, выставляем опцию.
            clusterize: true,
            // ObjectManager принимает те же опции, что и кластеризатор.
            gridSize: 32,
            clusterDisableClickZoom: true
        });


    // Чтобы задать опции одиночным объектам и кластерам,
    // обратимся к дочерним коллекциям ObjectManager.
    objectManager.objects.options.set('preset', 'islands#greenDotIcon');
    objectManager.clusters.options.set('preset', 'islands#greenClusterIcons');
    myMap.geoObjects.add(objectManager);

    $.ajax({
        url: `http://127.0.0.1:8000/api/cdek-pvz/?format=json&search=${city}`
    }).done(function (data) {
            var new_data = data.map(function (pvz, city_info) {

                    pvz = {
                        "type": "Feature",
                        "id": pvz.id,
                        "geometry": {
                            "type": "Point",
                            "coordinates": [pvz.latitude, pvz.longitude]
                        },
                        "properties": {
                            "balloonContentHeader": `<font size=3><b>Пункт выдачи СDEK ${pvz.title}</b></font>`,
                            "balloonContentBody": `<p>Адрес: ${pvz.address} </p><p> Стоимость доставки: ${cdekPrice} ₽</p> 
                                                    <p>График работы: ${pvz.work_time}</p>
                                                    <p>Срок доставки от ${String(city_info.delivery_period_min)} до ${String(city_info.delivery_period_max)} рабочих дней</p>
                                                    <small>Срок доставки указан без учета срока изготовления товара</small>
                                                    <input class="pvz" type="button" value="Забрать здесь" name="${pvz.code}" onclick="setpvz('${pvz.address}','${pvz.code}')">`,
                            "balloonContentFooter": "<font size=1>Сделано программистом </font> <strong>Barash.CO</strong>",

                        }
                    }

                    return (pvz)

                }
            )
            // alert(new_data[1])
            new_data = {
                "type": "FeatureCollection",
                "features": new_data
            }
            objectManager.add(new_data);

        }
    )


}


$(document).ready(function () {

        city = $('#id_city').val()
        region = $('#id_region').val().split(', ')[0]

        country = $('#id_country').val()

        if (city === 'Краснодар') {
            $('#courier-price').append(`300.00`)
            $('input[name=delivery_price_courier]').val(`300.00`)
        }

        // Установка цены на Почту России
        if (country === 'Россия') {
            $.ajax({
                url: `http://127.0.0.1:8000/api/russian-post-delivery/?search=${region}`
            }).done(function (data) {
                region_info = data[0]
                $('#russian-post-price').append(`${region_info.delivery_price}`);
                $('input[name=delivery_price_russian-post]').val(`${region_info.delivery_price}`);


            })
        } else {
            $('#russian-post-price').append(`1200.00`);
            $('input[name=delivery_price_post-price]').val(`1200.00`);

        }

        // Установка цены на СДЕК
        $.ajax({
            url: `http://127.0.0.1:8000/api/cdek-city/?format=json&search=${city}`
        }).done(function (data) {
                if (data.length !== 0) {
                    city_info = data[0]

                    $('#cdek-price').append(`${city_info.delivery_price}`);
                    $('#cdek-price').parent().append(`<div id="select-pvz"><div>`);
                    $('input[name=delivery_price_cdek]').val(`${city_info.delivery_price}`);


                    // Накидываем слушателя на кнопку СДЕКа для отображения карты
                    $('input[type=radio][name=delivery_choice]').change(function () {
                        if (this.value === 'cdek') {
                            $('#map').css("display", "block");

                        } else {
                            $('#map').css("display", "none");
                            $('#select-pvz').html(``)
                        }
                    });

                    setTimeout(() => {
                        init(city_info)
                    }, 2000);


                }
            }
        )

    }
)

