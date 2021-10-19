from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BaseView,
    MainPageView,
    ProductDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CreateOrder,
    GetAddressOrderView,
    GetDeliveryOrderView,
    AddDeliveryOrderView,
    LoginView,
    RegistrationView,
    CategoryView,
    DeliveryPaymentView,
    DeliveryCalculatorView,
    DistributorsView,
    PromocodeActivateView,
    PromocodeDeactivateView,
    ReloadCdekView
)


urlpatterns = [
    #path('', BaseView.as_view(), name='base'),
    path('', MainPageView.as_view(), name='main_page'),
    path('category/', CategoryView.as_view(), name = 'categories'),
    path('delivery-payment/', DeliveryPaymentView.as_view(), name = 'delivery_payment'),
    path('delivery-calculator/', DeliveryCalculatorView.as_view(), name = 'delivery-calculator'),
    path('distributors/', DistributorsView.as_view(), name = 'distributors'),
    #ЗДЕСЬ ct_model и slug это те самые, что мы создали в функции get_product_url в models
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('create-order/', CreateOrder.as_view(), name='create-order'),
    path('order-address/', GetAddressOrderView.as_view(), name='order-address'),
    path('order-delivery/', GetDeliveryOrderView.as_view(), name='order-delivery'),
    path('add-delivery/', AddDeliveryOrderView.as_view(), name='add-delivery'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('activate-promocode/', PromocodeActivateView.as_view(), name='activate-promocode'),
    path('deactivate-promocode/', PromocodeDeactivateView.as_view(), name='deactivate-promocode'),
    path('reload-cdek/', ReloadCdekView.as_view(), name='reload-cdek'),

]
