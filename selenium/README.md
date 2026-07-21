# Selenium & API Black Box Testing — TA Coffeeshop

Folder ini berisi **black box testing** untuk seluruh fitur sistem TA Coffeeshop menggunakan:
- **Selenium** (test antarmuka CI4 web)
- **pytest + requests** (test REST API Spring Boot)

## Struktur File

```
selenium/
├── requirements.txt        # Dependency Python
├── test_ci4_web.py         # Black box test CI4 Web (Selenium)
├── test_spring_api.py      # Black box test Spring Boot API (HTTP/requests)
└── README.md               # Panduan ini
```

## Prasyarat

1. **Python 3.8+** terinstal
2. **Google Chrome** terinstal (terbaru)
3. **Server Laragon** berjalan (untuk CI4 web test)
4. **Spring Boot** berjalan di port `8083` (untuk API test)
5. Database `ta_db_coffeeshop` sudah diinisialisasi dan ada user `admin`

---

## Cara Instalasi

```powershell
# Masuk ke folder selenium
cd c:\Dokumen\ta-server-coffeeshop\selenium

# Install dependencies
pip install -r requirements.txt
```

---

## Cara Menjalankan Test

### Test CI4 Web (Selenium Browser)

> Pastikan Laragon berjalan dan `http://ta-ci4-web-coffeeshop.test` dapat diakses.

```powershell
# Jalankan semua test CI4 (dengan jendela browser terlihat)
pytest test_ci4_web.py -v

# Jalankan dengan laporan HTML
pytest test_ci4_web.py -v --html=report_ci4.html --self-contained-html

# Jalankan headless (tanpa jendela browser)
# Edit HEADLESS = True di baris konfigurasi test_ci4_web.py
pytest test_ci4_web.py -v
```

### Test Spring Boot API (HTTP/requests)

> Pastikan Spring Boot sudah berjalan (`mvn spring-boot:run` di folder server).

```powershell
# Jalankan semua test API
pytest test_spring_api.py -v

# Dengan laporan HTML
pytest test_spring_api.py -v --html=report_api.html --self-contained-html

# Sesuaikan username/password admin di test_spring_api.py:
# ADMIN_USER = "admin"
# ADMIN_PASS = "admin123"
```

### Jalankan Semua Test Sekaligus

```powershell
pytest test_ci4_web.py test_spring_api.py -v --html=report_lengkap.html --self-contained-html
```

---

## Cakupan Test

### CI4 Web (`test_ci4_web.py`) — 39 Test Case

| Kelas | TC | Fitur yang Diuji |
|---|---|---|
| `TestHalaman` | 7 | Beranda, navbar, hero, about, menu, kontak, footer |
| `TestFilterMenu` | 5 | Filter Kopi, Non-Kopi, Pastry, Semua, Search |
| `TestKeranjangCheckout` | 8 | Cart, form checkout (pesanan), validasi field |
| `TestQRPaymentPage` | 4 | QR payment, success, pending, error page |
| `TestFormKontak` | 8 | Form kontak (pesan_kontak), validasi, isi field |
| `TestFooter` | 3 | Social media, nav link, kredit |
| `TestElementLainnya` | 3 | Hamburger, maps, modal produk |

### Spring Boot API (`test_spring_api.py`) — 33 Test Case

| Kelas | TC | Endpoint / Tabel |
|---|---|---|
| `TestAuth` | 3 | `POST /auth/login` → tabel `user` |
| `TestUser` | 3 | `GET /user` → tabel `user` |
| `TestMenuProduk` | 7 | CRUD `/menu-produk` → tabel `menu_produk` |
| `TestPesanan` | 7 | CRUD `/pesanan` → tabel `pesanan` |
| `TestDesainPesanan` | 5 | CRUD `/desain-pesanan` → tabel `desain_pesanan` |
| `TestPesanKontak` | 5 | CRUD `/pesan-kontak` → tabel `pesan_kontak` |
| `TestValidasiInput` | 3 | Validasi input kosong/tidak valid |

**Total: 72 Test Case**

---

## Konfigurasi

Edit variabel berikut di awal file masing-masing:

**`test_ci4_web.py`:**
```python
BASE_URL  = "http://ta-ci4-web-coffeeshop.test"
HEADLESS  = False   # True = tanpa jendela browser
```

**`test_spring_api.py`:**
```python
BASE_URL   = "http://127.0.0.1:8083/api"
ADMIN_USER = "admin"       # Username admin di database
ADMIN_PASS = "admin123"    # Password admin di database
```
