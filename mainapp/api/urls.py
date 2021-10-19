from django.urls import path

from .api_views import CategoryListApiView, ProductListApiView, PVZCDEKListApiView, CDEKCityListApiView, \
    RussianPostDeliveryListApiView

urlpatterns = [
    path('categories/', CategoryListApiView.as_view(), name='categories'),
    path('products/', ProductListApiView.as_view(), name='products'),
    path('cdek-pvz/', PVZCDEKListApiView.as_view(), name='cdek-pvz'),
    path('cdek-city/', CDEKCityListApiView.as_view(), name='cdek-city'),
    path('russian-post-delivery/', RussianPostDeliveryListApiView.as_view(), name='russian-post-delivery'),
]
