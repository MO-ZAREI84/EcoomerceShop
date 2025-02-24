from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('', views.home, name='home'),
    path('category/<slug:category_slug>', views.home, name='category_page'),
    path('product/<slug:category_slug>/<slug:product_slug>', views.product_page, name='product_page'),
    path('cart/add/<int:product_id>/',views.add_cart,name = 'add_cart'),
    path('cart/remove/<int:product_id>/',views.removed,name = 'removed'),
    path('cart/delete/<int:product_id>/',views.cart_remove_product ,name = 'Delete'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('account/create/',views.SignUpview,name = 'signup'),
    path('account/login/',views.signinview,name = 'signin'),

    
]
