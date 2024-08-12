from django.urls import path
from . import views

urlpatterns = [
    path('', views.beranda_admin, name='beranda_admin'),
    path('daftar/konsumen/admin', views.konsumen_admin, name='konsumen_admin'),
    path('daftar/hubungi-kami/admin', views.hubungi_admin, name='hubungi_admin'),
    path('daftar/transaksi/admin', views.transaksi_admin, name='transaksi_admin'),
    
    path('daftar/produk/admin', views.produk_list, name='produk_admin'),
    path('daftar/produk/admin/<int:pk>/', views.produk_detail, name='produk-detail'),
    path('daftar/produk/admin/create/', views.produk_create, name='produk-create'),
    path('daftar/produk/admin/update/<int:pk>/', views.produk_update, name='produk-update'),
    path('daftar/produk/admin/delete/<int:pk>/', views.produk_delete, name='produk-delete'),
    path('export/xlsx/', views.export_transaksi_xlsx, name='export_transaksi_xlsx'),
    
    path('logout/', views.logoutpage, name='logoutpage'),
]