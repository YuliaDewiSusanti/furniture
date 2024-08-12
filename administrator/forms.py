from django import forms
from website.models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['kategori', 'nama_produk', 'gambar', 'gambar_satu', 
                  'gambar_dua', 'gambar_tiga', 'gambar_empat', 'keterangan', 'harga', 
                  'no_whatsup', 'diskon', 'keterangan_barang'
                  , 'warna', 'bahan', 'ukuran', 'unit_ukuran']
        widgets = {
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'nama_produk': forms.TextInput(attrs={'class': 'form-control'}),
            'gambar': forms.FileInput(attrs={'class': 'form-control'}),
            'gambar_satu': forms.FileInput(attrs={'class': 'form-control'}),
            'gambar_dua': forms.FileInput(attrs={'class': 'form-control'}),
            'gambar_tiga': forms.FileInput(attrs={'class': 'form-control'}),
            'gambar_empat': forms.FileInput(attrs={'class': 'form-control'}),
            'keterangan': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description here...'
            }),
            'harga': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_whatsup': forms.NumberInput(attrs={'class': 'form-control'}),
            'diskon': forms.NumberInput(attrs={'class': 'form-control'}),
            'keterangan_barang': forms.Select(attrs={'class': 'form-control'}),
            'warna': forms.TextInput(attrs={'class': 'form-control'}),
            'bahan': forms.TextInput(attrs={'class': 'form-control'}),
            'ukuran': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_ukuran': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'kategori': 'Category',
            'nama_produk': 'Product Name',
            'gambar': 'Image (200x200 px)',
            'gambar_satu': 'Image 1 (575x200 px)',
            'gambar_dua': 'Image 2 (575x200 px)',
            'gambar_tiga': 'Image 3 (575x200 px)',
            'gambar_empat': 'Image 4 (575x200 px)',
            'keterangan': 'Description',
            'harga': 'Price',
            'no_whatsup': 'WhatsApp Number',
            'diskon': 'Discount',
            'keterangan_barang': 'Condition',
            'warna': 'Color',
            'bahan': 'Material',
            'ukuran': 'Size',
            'unit_ukuran': 'Size Unit',
        }
