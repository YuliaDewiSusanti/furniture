from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import tolakhalaman_ini, ijinkan_pengguna
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from cart.forms import CartAddProductForm
from cart.keranjang import Cart
from .models import Produk, Kategori, Kontak, Profil, Slide, Statis, ChatID, Custumer
from cart.models import Transaksi, DetailTransaksi
from django.views.generic import View
from django.db.models import Count 
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.humanize.templatetags.humanize import intcomma
from .telegram_utill import send_telegram_message
from django.core.paginator import Paginator
from midtransclient import Snap
from django.views.decorators.csrf import csrf_exempt
import json
import time
from django.conf import settings
import midtransclient
from django.http import JsonResponse

def beranda(request):
    kategori = Kategori.objects.filter(aktif=True).order_by('-id')
    slider = Slide.objects.filter(aktif=True).order_by('-id')
    jumlahkategori = Kategori.objects.all().annotate(produk_count=Count('produks')).order_by('-id')
    produk = Produk.objects.order_by('-id')
    cart_product_form = CartAddProductForm()
    context = {
            "judul": "Halaman Beranda",
            "kategori" : kategori,
            "judul": "Halaman Beranda",
            "jumlahkategori": jumlahkategori,
            "slide": slider,
            "produk": produk,
            "cart_product_form": cart_product_form,
            "id": "home"
    }
    return render(request, 'beranda.html', context)

@tolakhalaman_ini
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.error(request, 'Username Tidak ditemukan')
            return redirect('loginpage')
        
        cocokan = authenticate(request, username=username, password=password)
        if cocokan is None:
            messages.error(request, 'Usernama dana Password yang anda masukan salah')
            return redirect('loginpage')
        if cocokan is not None:
            login(request, cocokan)
            return redirect('beranda_admin')
    context = {
        'judul': 'Login',
    }
    return render(request, 'login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

@tolakhalaman_ini
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        nama = request.POST['nama']
        wa = request.POST['wa']
        alamat = request.POST['alamat']
        email = request.POST['email']
        group_name = 'custumer'  # Nama grup yang ingin Anda gunakan

        if password != password2:
            messages.error(request, 'Password and Confirm Password do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')

        # Simpan user

       
        user = User.objects.create_user(username=username, password=password)
        # Tambahkan data tambahan
        user.first_name = nama
        user.email = email
        user.save()
        pelanggan = Custumer.objects.create(user=user, nama=password, wa=wa, alamat=alamat, email=email)
        # Tambahkan user ke grup
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

        messages.success(request, 'Registration successful. You can now login.')
        return redirect('loginpage')
    else:
        return render(request, 'register.html')

def profil(request):
    profil = Profil.objects.all().order_by('-id')[:1]
    context = {
            "judul": "Halaman Tentang Kami",
            "profil": profil,
            "id": "about-us"
    }
    return render(request, 'profil.html', context)

# def kontak(request):
#     context = {
#             "judul": "Halaman Hubungi Kami",
#             "id": "contact"
#     }
#     return render(request, 'kontak.html', context)

class KontakView(View):
    def get(self, request):
        context = {
            "judul": "Halaman Hubungi Kami",
            "id": "contact"
        }
        return render(request, 'kontak.html', context)
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        data = Kontak.objects.create(nama = name, email = email, telpon = phone, subjek = subject, isi = message)
        data.save
        return redirect('kontak')

def produk(request, kategori_slug, slug):
    produk = get_object_or_404(Produk, slug=slug)
    context = {
        "judul": "Halaman Produk Kami",
        "produk": produk,
        "id": "product-detail"
    }
    return render(request, 'produk.html', context)

def pemesanan(request):
    context = {
            "judul": "Halaman Pemesanan Kami",
            "class": "product-cart checkout-cart"
    }
    return render(request, 'pemesanan.html', context)

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        snap = midtransclient.Snap(
            is_production=settings.MIDTRANS['IS_PRODUCTION'],
            server_key=settings.MIDTRANS['SERVER_KEY']
        )

        order_id = 'order-' + str(int(time.time()))
        gross_amount = int(request.POST.get('grantotal', 0))

        transaction_data = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": gross_amount
            },
            "credit_card": {
                "secure": True
            },
            "customer_details": {
                "first_name": request.POST.get('nama_depan'),
                "last_name": request.POST.get('nama_belakang'),
                "email": request.POST.get('email'),
                "phone": request.POST.get('telpon')
            }
        }

        try:
            transaction = snap.create_transaction(transaction_data)
            transaction_token = transaction.get('token', '')
            payment_url = transaction.get('redirect_url', '')

            if transaction_token:
                # Simpan data ke model Transaksi
                transaksi = Transaksi(
                    no_transaksi=order_id,
                    nama_depan=request.POST.get('nama_depan'),
                    nama_belakang=request.POST.get('nama_belakang'),
                    alamat=request.POST.get('alamat'),
                    provinsi=request.POST.get('provinsi'),
                    kabupaten=request.POST.get('kabupaten'),
                    kecamatan=request.POST.get('kecamatan'),
                    kode_post=request.POST.get('kode_pos'),
                    email=request.POST.get('email'),
                    whatsapp=request.POST.get('telpon'),
                    total_transaksi=gross_amount,
                    status='Baru',
                    tanggal_kirim=datetime.datetime.now()  # Atur tanggal kirim sesuai kebutuhan
                )
                transaksi.save()

                return JsonResponse({"payment_url": payment_url})
            else:
                return JsonResponse({"error": "Failed to get transaction token"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    context = {
        "judul": "Halaman Checkout Kami",
        "class": "product-checkout"
    }
    return render(request, 'checkout.html', context)

@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        notification_json = json.loads(request.body)
        transaction_status = notification_json['transaction_status']
        order_id = notification_json['order_id']

        if transaction_status == 'settlement':
            # Update status pesanan menjadi terbayar
            # Misalnya: update_order_status(order_id, 'paid')
            return HttpResponse('OK')

    return HttpResponse('Error')


def kategori(request, slug):
    kategori = get_object_or_404(Kategori, slug=slug)
    produk = kategori.produks.order_by('-id')
    halaman_tampil = Paginator(produk, 6)
    halaman_url = request.GET.get('halaman', 1)
    halaman_produk = halaman_tampil.get_page(halaman_url)
    cart_product_form = CartAddProductForm()
    if halaman_produk.has_previous():
        url_previous = f'?halaman={halaman_produk.previous_page_number()}'
    else:
        url_previous = ''
    if halaman_produk.has_next():
        url_next = f'?halaman={halaman_produk.next_page_number()}'
    else:
        url_next = ''
    context = {
        "judul": "Halaman Kategori",
        "detailkategori": kategori,
        "produk": halaman_produk,
        "previous": url_previous,
        "next": url_next,
        "cart_product_form": cart_product_form,
        "id": "product-sidebar-left"
    }
    return render(request, 'kategori.html', context)

def kategoriberanda(request):
        kategori = Kategori.objects.filter(aktif=True).order_by('-id')
        return {'kategori':kategori}

def modalberita(request):
        modalproduk = Produk.objects.order_by('-id')
        return {'modalproduk':modalproduk}

def statisweb(request):
        statis = Statis.objects.get(id=1) 
        return {'statis':statis}

class CheckoutView(View):
    def get(self, request):
        context = {
            'judul': 'Halaman Checkout',
            "class": "product-checkout"
        }
        return render(request, 'checkout.html', context)

    def post(self, request):
        grantotal = request.POST.get('grantotal')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        alamat = request.POST.get('alamat')
        provinsi = request.POST.get('provinsi')
        kabupaten = request.POST.get('kabupaten')
        kecamatan = request.POST.get('kecamatan')
        kode_post = request.POST.get('kode_post')
        email = request.POST.get('email')
        telpon = request.POST.get('telpon')
        no_transaksi = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        transaksi = Transaksi.objects.create(
            no_transaksi=no_transaksi,
            nama_depan=nama_depan,
            nama_belakang=nama_belakang,
            alamat=alamat,
            provinsi=provinsi,
            kabupaten=kabupaten,
            kecamatan=kecamatan,
            kode_post=kode_post,
            email=email,
            telpon=telpon,
            total_transaksi=grantotal)
        transaksi.save()

        keranjang = Cart(request)
        for r in keranjang:
            instance_detail = DetailTransaksi(
                no_transaksi=no_transaksi,
                produk=r['product'],
                jumlah=r['quantity'],
            )
            instance_detail.save()

        chats = ChatID.objects.filter(aktif=True)
        for chat in chats:
            grantotal_formatted = f"Rp. {intcomma(grantotal)}"
            message = f"Assalamualaikum Wr Wb,\n\nNo Transaksi: <b>{no_transaksi}</b>\nNama: <b>{nama_depan} {nama_belakang}</b>\nNo Telepon: <b>{telpon}</b>\nAlamat: <b>{alamat}</b>\nTotal Transaksi: <b>{grantotal_formatted}</b>\n\nTerimakasih, Salam Furniture Store dan Wssalamualaikum Wr Wb."
            send_telegram_message(chat.chatid, message)

        keranjang.clear()
        return redirect("checkout")

@login_required
def histori_pembayaran(request):
    transaksi = Transaksi.objects.order_by('-tanggal_kirim')
    context = {
        'judul': 'Histori Pembayaran',
        'transaksi': transaksi,
        'id' : 'about-us'
    }
    return render(request, 'histori_pembayaran.html', context)