from django.shortcuts import render, get_object_or_404, redirect
from website.models import *
from cart.models import *
# from .forms import KategoriForm, ProdukForm, SlideForm
from django.contrib.auth.decorators import login_required
from website.decorators import ijinkan_pengguna,pilihan_login
from django.db.models import Count, Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import logout
import json
import openpyxl
import datetime
from django.utils import dateformat

from datetime import date
from datetime import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment
from django.urls import reverse
from .forms import *
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.utils import timezone

@login_required(login_url='loginpage')
@pilihan_login
def beranda_admin(request):
    jmlKategori = Kategori.objects.filter(aktif=True).count()
    jmlCustumer = Custumer.objects.count()
    jmlProduk = Produk.objects.count()
    jmlTransaksi = Transaksi.objects.count()

    context = {
        'judul': 'Halaman Beranda',
        'menu': 'beranda',
        'jmlKategori':jmlKategori,
        'jmlCustumer':jmlCustumer,
        'jmlProduk':jmlProduk,
        'jmlTransaksi':jmlTransaksi,
        'current_date': timezone.now().strftime('%Y-%m-%d'),
        'website_usage': User.objects.filter(is_active=True).count(),
    }
    return render(request, 'admin_beranda.html', context)

def produk_list(request):
    produk_list = Produk.objects.order_by('-id')
    paginator = Paginator(produk_list, 10)  # Show 10 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'judul': 'Halaman Produk',
        'menu': 'produk',
        'data': page_obj,
    }
    return render(request, 'admin_produk.html', context)

def produk_detail(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    context = {
        'judul': 'Halaman Produk',
        'menu': 'produk',
        'produk': produk
    }
    return render(request, 'produk_detail.html', context)

def produk_create(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES)
        if form.is_valid():
            produk = form.save(commit=False)
            produk.slug = slugify(produk.nama_produk)
            produk.save()
            return redirect('produk_admin')
        else:
            print(form.errors)  # Debugging
    else:
        form = ProdukForm()

    context = {
        'judul': 'Halaman Tambah Produk',
        'menu': 'produk',
        'form': form
    }
    return render(request, 'produk_form.html', context)

def produk_update(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('produk-detail', pk=pk)
    else:
        form = ProdukForm(instance=produk)
    context = {
        'judul': 'Halaman Produk',
        'menu': 'produk',
        'form': form
    }
    return render(request, 'produk_form.html', context)


def produk_delete(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        produk.delete()
        return redirect('produk_admin')
    context = {
        'judul': 'Halaman Produk',
        'menu': 'produk',
        'produk': produk
    }
    return render(request, 'produk_confirm_delete.html', context)


def konsumen_admin(request):
    customer_list = Custumer.objects.all()
    
    # Atur pagination
    paginator = Paginator(customer_list, 10)  # 10 customer per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'judul': 'Halaman Pelanggan',
        'menu': 'konsumen',
        'data': page_obj
    }
    return render(request, 'admin_konsumen.html', context)

def hubungi_admin(request):
    kontak_list = Kontak.objects.all()
    
    # Atur pagination
    paginator = Paginator(kontak_list, 10)  # 10 customer per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'judul': 'Halaman Hubungi Kami',
        'menu': 'kontak',
        'data': page_obj
    }
    return render(request, 'admin_kontak.html', context)

def transaksi_admin(request):
    list = Transaksi.objects.order_by('-id')
    
    # Atur pagination
    paginator = Paginator(list, 10)  # 10 customer per halaman
    page_number = request.GET.get('page')


    page_obj = paginator.get_page(page_number)

    context = {
        'judul': 'Halaman Hubungi Kami',
        'menu': 'transaksi',
        'data': page_obj
    }
    return render(request, 'admin_transaksi.html', context)


def logoutpage(request):
    logout(request)
    return redirect('loginpage')


def export_transaksi_xlsx(request):
    # Create a workbook and an active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Transaksi'

    # Define the titles for columns
    columns = ['No Transaksi', 'Nama Lengkap', 'Alamat', 'Email', 'WhatsApp', 'Total Transaksi', 'Status']
    worksheet.append(columns)

    # Fetch the data from your model
    transaksi_list = Transaksi.objects.all()

    # Loop through the transactions and write data to the Excel file
    for transaksi in transaksi_list:
        worksheet.append([
            transaksi.no_transaksi,
            f"{transaksi.nama_depan} {transaksi.nama_belakang}",
            transaksi.alamat,
            transaksi.email,
            transaksi.whatsapp,
            transaksi.total_transaksi,
            transaksi.status
        ])

    # Set the response to return the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transaksi.xlsx'
    workbook.save(response)
    
    return response