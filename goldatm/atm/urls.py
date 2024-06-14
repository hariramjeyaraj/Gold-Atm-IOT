from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name= 'home'),
    path('/atm/api',atm,name='atm'),
    path('login/', login,name="login"),
    # path('otp/', otp,name="otp"),
    path('categories/',categories,name='categories'),
    path('bullion/',bullion,name='bullion'),
    path('silver/',silver,name='silver'),
    path('product/',product,name='product'),
    path('product2/',product2,name='product2'),
    path('payment_view/',payment_view,name='payment_view'),
    path('payment/', payment_view, name='payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
    # path('pay/',pay, name="pay"),
    path('success/',success,name='success'),
    path('machine/',machine,name='machine'),
    path('thanku',thanku,name='thanku')



]

