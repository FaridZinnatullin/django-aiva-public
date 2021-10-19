from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Distributor)
admin.site.register(Collection)
admin.site.register(Article)
admin.site.register(Feedback)
admin.site.register(Series)
admin.site.register(TypeSkin)
admin.site.register(Size)
admin.site.register(Problem)
admin.site.register(TypeProduct)
admin.site.register(Purpose)
admin.site.register(TypeHair)
admin.site.register(RussianPostDelivery)
admin.site.register(Questionnaire)
admin.site.register(CDEKAuth)
admin.site.register(CDEKDeliveryPrice)
admin.site.register(CDEKRegions)
admin.site.register(CDEKCities)
admin.site.register(CDEK_PVZ)
admin.site.register(CDEKOrder)
admin.site.register(CDEKCountry)
admin.site.register(Promocode)
admin.site.register(TypeOfPromocode)
admin.site.register(TypeOfDelivery)



