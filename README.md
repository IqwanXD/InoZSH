# InoZSH

Tema dan konfigurasi Zsh otomatis untuk **Termux** (Android) dengan tampilan modern.

## ✨ Fitur

- 🎨 **Powerlevel10k**: Tema Zsh yang cepat dan informatif.
- 🔤 **Font Kustom**: Mendukung Nerd Font agar ikon tampil sempurna.
- ⚙️ **Otomatis**: Skrip Python mengatur semuanya dari instalasi hingga konfigurasi.
- 📦 **Siap Pakai**: Langsung terpasang dengan satu perintah.

## 📋 Prasyarat

- Termux (Android)
- Python 3

## 🚀 Instalasi

1. Clone repositori ini:
   ~~~bash
   git clone https://github.com/IqwanXD/InoZSH.git
   cd InoZSH
   ~~~

2. Jalankan skrip setup:
   ~~~bash
   python inozsh.py
   ~~~

3. Ikuti instruksi di layar. Skrip akan:
   - Memperbarui paket Termux.
   - Menginstal Zsh, Oh My Zsh, dan Powerlevel10k.
   - Menyalin font kustom ke Termux.
   - Menerapkan konfigurasi `zshrc` dan `p10k.zsh`.

4. Restart Termux atau jalankan `zsh` untuk melihat hasilnya.

## 📁 Struktur Repositori

~~~text
InoZSH/
├── config/
│   ├── font.ttf      # Font kustom (Nerd Font)
│   ├── p10k.zsh      # Konfigurasi Powerlevel10k
│   └── zshrc         # Konfigurasi Zsh
└── inozsh.py         # Skrip installer otomatis
~~~

## 🛠️ Kustomisasi

- Edit `config/zshrc` untuk alias dan pengaturan Zsh.
- Edit `config/p10k.zsh` untuk mengubah tampilan prompt.
- Ganti `config/font.ttf` dengan font favoritmu (pastikan mendukung Nerd Font).

## 📄 Lisensi

Proyek ini bebas digunakan dan dimodifikasi untuk keperluan pribadi.
