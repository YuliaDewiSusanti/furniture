from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required
from cart import views as cart_views

urlpatterns = [
    path('login/', views.loginpage, name='loginpage'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutpage, name='logoutpage'),
    path('', views.beranda, name='beranda'),
    path('profil-kami', views.profil, name='profil'),
    path('<slug:kategori_slug>/<slug:slug>', views.produk, name='produk'),
    # path('hubungi-kami', views.Kontak, name='kontak'),
    path('hubungi-kami', views.KontakView.as_view(), name='kontak'),
    
    path('produk-kami', views.produk, name='produk'),
    path('pemesanan-kami', views.pemesanan, name='pemesanan'),
    path('checkout', views.checkout, name='checkout'),
    path('payment-notification/', views.payment_notification, name='payment_notification'),
    path('histori-pembayaran', views.histori_pembayaran, name='histori_pembayaran'),  # Make sure this is correctly defined
    path('<slug:slug>', views.kategori, name='kategori'),
    
    path('add/<int:product_id>', cart_views.cart_add, name='cart_add'),
    path('remove/<int:product_id>', cart_views.cart_remove, name='cart_remove'),
    path('detail/', cart_views.cart_detail, name='cart_detail'),
]
