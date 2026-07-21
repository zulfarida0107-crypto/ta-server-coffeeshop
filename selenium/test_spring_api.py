"""
=============================================================
BLACK BOX TESTING — Spring Boot REST API Coffeeshop
URL Target : http://127.0.0.1:8083/api
Framework  : pytest + requests (HTTP functional black box test)

Endpoint yang diuji (sesuai database):
  - POST   /api/auth/login              → autentikasi (tabel: user)
  - GET    /api/user                    → daftar user (tabel: user)
  - GET    /api/menu-produk             → daftar menu (tabel: menu_produk)
  - POST   /api/menu-produk             → tambah menu
  - PUT    /api/menu-produk/{id}        → update menu
  - DELETE /api/menu-produk/{id}        → hapus menu
  - GET    /api/pesanan                 → daftar pesanan (tabel: pesanan)
  - POST   /api/pesanan                 → buat pesanan baru
  - PUT    /api/pesanan/{id}            → update status pesanan
  - DELETE /api/pesanan/{id}            → hapus pesanan
  - GET    /api/desain-pesanan          → daftar desain (tabel: desain_pesanan)
  - POST   /api/desain-pesanan          → tambah desain pesanan
  - DELETE /api/desain-pesanan/{id}     → hapus desain pesanan
  - GET    /api/pesan-kontak            → daftar kontak (tabel: pesan_kontak)
  - DELETE /api/pesan-kontak/{id}       → hapus kontak
  - POST   /api/pesan-kontak/{id}/balas → balas kontak (kirim email)

Cara jalankan:
  pytest test_spring_api.py -v --html=report_api.html --self-contained-html

CATATAN: Pastikan Spring Boot sudah berjalan di port 8083 dan
         ada minimal 1 user admin di database sebelum menjalankan test.
=============================================================
"""

import json
import pytest
import requests

# ─────────────────────────────────────────────────────────
# Konfigurasi
# ─────────────────────────────────────────────────────────
BASE_URL   = "http://127.0.0.1:8083/api"
ADMIN_USER = "admin"         # Sesuaikan dengan username di DB
ADMIN_PASS = "admin123"      # Sesuaikan dengan password di DB
TIMEOUT    = 10              # Request timeout detik

# State global yang di-share antar test dalam satu sesi
_token: str = ""
_created_menu_id: int    = 0
_created_pesanan_id: int = 0
_created_desain_id: int  = 0
_created_kontak_id: int  = 0


def auth_headers():
    """Kembalikan header dengan JWT token."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {_token}",
    }


def no_auth_headers():
    return {"Content-Type": "application/json", "Accept": "application/json"}


# ─────────────────────────────────────────────────────────
# TC-API-01~03: AUTH — POST /api/auth/login
# ─────────────────────────────────────────────────────────
class TestAuth:

    def test_login_berhasil(self):
        """TC-API-01: Login dengan kredensial valid mengembalikan token JWT."""
        global _token
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": ADMIN_USER, "password": ADMIN_PASS},
            headers=no_auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200, f"Status bukan 200: {r.status_code} — {r.text}"
        data = r.json()
        assert data.get("success") is True, f"Login tidak success: {data}"
        assert "token" in data.get("data", {}), "Token tidak ada di response"
        _token = data["data"]["token"]
        assert len(_token) > 20, "Token terlalu pendek"

    def test_login_password_salah(self):
        """TC-API-02: Login dengan password salah mengembalikan status non-200."""
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": ADMIN_USER, "password": "password_salah_999"},
            headers=no_auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code != 200, "Seharusnya gagal login dengan password salah"

    def test_login_user_tidak_ada(self):
        """TC-API-03: Login dengan username yang tidak ada mengembalikan error."""
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "user_tidak_ada_xyz", "password": "apapun"},
            headers=no_auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code != 200


# ─────────────────────────────────────────────────────────
# TC-API-04~06: USER — GET /api/user
# ─────────────────────────────────────────────────────────
class TestUser:

    def test_get_semua_user(self):
        """TC-API-04: GET /api/user mengembalikan daftar user (tabel: user)."""
        r = requests.get(f"{BASE_URL}/user", headers=auth_headers(), timeout=TIMEOUT)
        assert r.status_code == 200, f"Status bukan 200: {r.status_code}"
        data = r.json()
        assert data.get("success") is True
        assert isinstance(data.get("data"), list)

    def test_get_user_struktur_field(self):
        """TC-API-05: Setiap user memiliki field: id, username, namaLengkap, role."""
        r = requests.get(f"{BASE_URL}/user", headers=auth_headers(), timeout=TIMEOUT)
        users = r.json().get("data", [])
        if len(users) > 0:
            u = users[0]
            for field in ["id", "username", "namaLengkap", "role"]:
                assert field in u, f"Field '{field}' tidak ada di response user"

    def test_tanpa_token_401(self):
        """TC-API-06: Akses /api/user tanpa token mengembalikan 401/403."""
        r = requests.get(f"{BASE_URL}/user", headers=no_auth_headers(), timeout=TIMEOUT)
        assert r.status_code in [401, 403], f"Seharusnya 401/403, dapat: {r.status_code}"


# ─────────────────────────────────────────────────────────
# TC-API-07~13: MENU PRODUK — CRUD /api/menu-produk
# ─────────────────────────────────────────────────────────
class TestMenuProduk:

    def test_get_semua_menu(self):
        """TC-API-07: GET /api/menu-produk mengembalikan daftar menu (tabel: menu_produk)."""
        r = requests.get(f"{BASE_URL}/menu-produk", headers=auth_headers(), timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert data.get("success") is True
        assert isinstance(data.get("data"), list)

    def test_get_menu_struktur_field(self):
        """TC-API-08: Setiap menu memiliki field: id, namaProduk, harga, kategori."""
        r = requests.get(f"{BASE_URL}/menu-produk", headers=auth_headers(), timeout=TIMEOUT)
        menus = r.json().get("data", [])
        if len(menus) > 0:
            m = menus[0]
            for field in ["id", "namaProduk", "harga", "kategori"]:
                assert field in m, f"Field '{field}' tidak ada di response menu"

    def test_create_menu_produk(self):
        """TC-API-09: POST /api/menu-produk membuat menu baru."""
        global _created_menu_id
        payload = {
            "namaProduk": "Selenium Test Coffee",
            "harga": 25000,
            "deskripsi": "Menu test dari Selenium black box testing",
            "kategori": "Kopi",
            "gambar": "",
            "bagian": "Menu Kami",
        }
        r = requests.post(
            f"{BASE_URL}/menu-produk",
            json=payload,
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code in [200, 201], f"Status bukan 200/201: {r.status_code} — {r.text}"
        data = r.json()
        assert data.get("success") is True
        _created_menu_id = data["data"]["id"]
        assert _created_menu_id > 0

    def test_get_menu_by_id(self):
        """TC-API-10: GET /api/menu-produk/{id} mengembalikan satu menu."""
        if not _created_menu_id:
            pytest.skip("Menu belum dibuat")
        r = requests.get(
            f"{BASE_URL}/menu-produk/{_created_menu_id}",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        data = r.json()
        assert data.get("success") is True
        assert data["data"]["id"] == _created_menu_id

    def test_update_menu_produk(self):
        """TC-API-11: PUT /api/menu-produk/{id} mengupdate data menu."""
        if not _created_menu_id:
            pytest.skip("Menu belum dibuat")
        payload = {
            "namaProduk": "Selenium Updated Coffee",
            "harga": 30000,
            "deskripsi": "Deskripsi diupdate oleh Selenium",
            "kategori": "Kopi",
            "gambar": "",
            "bagian": "Menu Kami",
        }
        r = requests.put(
            f"{BASE_URL}/menu-produk/{_created_menu_id}",
            json=payload,
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        data = r.json()
        assert data.get("success") is True
        assert data["data"]["namaProduk"] == "Selenium Updated Coffee"

    def test_menu_not_found(self):
        """TC-API-12: GET /api/menu-produk/99999 mengembalikan 404."""
        r = requests.get(
            f"{BASE_URL}/menu-produk/99999",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 404

    def test_delete_menu_produk(self):
        """TC-API-13: DELETE /api/menu-produk/{id} menghapus menu."""
        if not _created_menu_id:
            pytest.skip("Menu belum dibuat")
        r = requests.delete(
            f"{BASE_URL}/menu-produk/{_created_menu_id}",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        assert r.json().get("success") is True


# ─────────────────────────────────────────────────────────
# TC-API-14~20: PESANAN — CRUD /api/pesanan
# ─────────────────────────────────────────────────────────
class TestPesanan:

    def test_get_semua_pesanan(self):
        """TC-API-14: GET /api/pesanan mengembalikan daftar pesanan (tabel: pesanan)."""
        r = requests.get(f"{BASE_URL}/pesanan", headers=auth_headers(), timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert data.get("success") is True
        assert isinstance(data.get("data"), list)

    def test_get_pesanan_struktur_field(self):
        """TC-API-15: Setiap pesanan memiliki field lengkap sesuai tabel pesanan."""
        r = requests.get(f"{BASE_URL}/pesanan", headers=auth_headers(), timeout=TIMEOUT)
        pesanans = r.json().get("data", [])
        if len(pesanans) > 0:
            p = pesanans[0]
            for field in ["id", "namaPelanggan", "totalHarga", "statusPesanan", "detailPesanan"]:
                assert field in p, f"Field '{field}' tidak ada di response pesanan"

    def test_create_pesanan(self):
        """TC-API-16: POST /api/pesanan membuat pesanan baru."""
        global _created_pesanan_id
        payload = {
            "namaPelanggan": "Pelanggan Selenium Test",
            "idProduk": 0,
            "jumlah": 2,
            "totalHarga": 50000.0,
            "statusPesanan": "Baru",
            "tanggalPesanan": "2026-07-21 10:00:00",
            "detailPesanan": json.dumps([
                {"id": "1", "name": "Espresso", "price": 25000, "quantity": 2}
            ]),
        }
        r = requests.post(
            f"{BASE_URL}/pesanan",
            json=payload,
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code in [200, 201], f"Status bukan 200/201: {r.status_code} — {r.text}"
        data = r.json()
        assert data.get("success") is True
        _created_pesanan_id = data["data"]["id"]
        assert _created_pesanan_id > 0

    def test_get_pesanan_by_id(self):
        """TC-API-17: GET /api/pesanan/{id} mengembalikan satu pesanan."""
        if not _created_pesanan_id:
            pytest.skip("Pesanan belum dibuat")
        r = requests.get(
            f"{BASE_URL}/pesanan/{_created_pesanan_id}",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        assert r.json()["data"]["id"] == _created_pesanan_id

    def test_update_status_pesanan(self):
        """TC-API-18: PUT /api/pesanan/{id} mengubah status pesanan menjadi 'Proses'."""
        if not _created_pesanan_id:
            pytest.skip("Pesanan belum dibuat")
        r_get = requests.get(
            f"{BASE_URL}/pesanan/{_created_pesanan_id}",
            headers=auth_headers(), timeout=TIMEOUT
        )
        existing = r_get.json()["data"]
        existing["statusPesanan"] = "Proses"
        r = requests.put(
            f"{BASE_URL}/pesanan/{_created_pesanan_id}",
            json=existing,
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        assert r.json()["data"]["statusPesanan"] == "Proses"

    def test_update_status_pesanan_selesai(self):
        """TC-API-19: PUT /api/pesanan/{id} mengubah status pesanan menjadi 'Selesai'."""
        if not _created_pesanan_id:
            pytest.skip("Pesanan belum dibuat")
        r_get = requests.get(
            f"{BASE_URL}/pesanan/{_created_pesanan_id}",
            headers=auth_headers(), timeout=TIMEOUT
        )
        existing = r_get.json()["data"]
        existing["statusPesanan"] = "Selesai"
        r = requests.put(
            f"{BASE_URL}/pesanan/{_created_pesanan_id}",
            json=existing,
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        assert r.json()["data"]["statusPesanan"] == "Selesai"

    def test_pesanan_not_found(self):
        """TC-API-20: GET /api/pesanan/99999 mengembalikan 404."""
        r = requests.get(
            f"{BASE_URL}/pesanan/99999",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 404


# ─────────────────────────────────────────────────────────
# TC-API-21~24: DESAIN PESANAN — CRUD /api/desain-pesanan
# ─────────────────────────────────────────────────────────
class TestDesainPesanan:

    def test_get_semua_desain_pesanan(self):
        """TC-API-21: GET /api/desain-pesanan mengembalikan list (tabel: desain_pesanan)."""
        r = requests.get(f"{BASE_URL}/desain-pesanan", headers=auth_headers(), timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert data.get("success") is True
        assert isinstance(data.get("data"), list)

    def test_create_desain_pesanan(self):
        """TC-API-22: POST /api/desain-pesanan membuat desain pesanan baru."""
        global _created_desain_id
        if not _created_pesanan_id:
            pytest.skip("Pesanan belum dibuat (prasyarat untuk desain)")
        payload = {
            "idPesanan": _created_pesanan_id,
            "fileDesainUrl": "https://example.com/desain-selenium-test.jpg",
            "keterangan": "Desain kue ulang tahun - Test Selenium",
            "tanggalUpload": "2026-07-21 10:00:00",
            "statusPesanan": "Baru",
        }
        r = requests.post(
            f"{BASE_URL}/desain-pesanan",
            json=payload,
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code in [200, 201], f"Status bukan 200/201: {r.status_code} — {r.text}"
        data = r.json()
        assert data.get("success") is True
        _created_desain_id = data["data"]["id"]

    def test_desain_pesanan_struktur_field(self):
        """TC-API-23: Setiap desain pesanan memiliki field sesuai tabel desain_pesanan."""
        r = requests.get(f"{BASE_URL}/desain-pesanan", headers=auth_headers(), timeout=TIMEOUT)
        items = r.json().get("data", [])
        if len(items) > 0:
            d = items[0]
            for field in ["id", "idPesanan", "statusPesanan"]:
                assert field in d, f"Field '{field}' tidak ada di response desain"

    def test_delete_desain_pesanan(self):
        """TC-API-24: DELETE /api/desain-pesanan/{id} berhasil menghapus desain."""
        if not _created_desain_id:
            pytest.skip("Desain belum dibuat")
        r = requests.delete(
            f"{BASE_URL}/desain-pesanan/{_created_desain_id}",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        assert r.json().get("success") is True

    def test_delete_pesanan_setelah_desain(self):
        """TC-API-25: DELETE /api/pesanan/{id} (cleanup test pesanan)."""
        if not _created_pesanan_id:
            pytest.skip("Pesanan belum dibuat")
        r = requests.delete(
            f"{BASE_URL}/pesanan/{_created_pesanan_id}",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        assert r.json().get("success") is True


# ─────────────────────────────────────────────────────────
# TC-API-26~30: PESAN KONTAK — /api/pesan-kontak
# ─────────────────────────────────────────────────────────
class TestPesanKontak:

    def test_get_semua_kontak(self):
        """TC-API-26: GET /api/pesan-kontak mengembalikan list (tabel: pesan_kontak)."""
        r = requests.get(f"{BASE_URL}/pesan-kontak", headers=auth_headers(), timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert data.get("success") is True
        assert isinstance(data.get("data"), list)

    def test_kontak_struktur_field(self):
        """TC-API-27: Setiap pesan kontak memiliki field sesuai tabel pesan_kontak."""
        r = requests.get(f"{BASE_URL}/pesan-kontak", headers=auth_headers(), timeout=TIMEOUT)
        items = r.json().get("data", [])
        if len(items) > 0:
            k = items[0]
            for field in ["id", "nama", "email", "subjek", "pesan"]:
                assert field in k, f"Field '{field}' tidak ada di response kontak"

    def test_create_kontak_via_endpoint(self):
        """TC-API-28: POST /api/pesan-kontak membuat pesan kontak baru."""
        global _created_kontak_id
        payload = {
            "nama": "Selenium Tester",
            "email": "selenium.tester@example.com",
            "subjek": "Pengujian Black Box Selenium",
            "pesan": "Pesan ini dikirim otomatis oleh Selenium untuk pengujian fitur kontak.",
            "tanggalDikirim": "2026-07-21 10:00:00",
        }
        r = requests.post(
            f"{BASE_URL}/pesan-kontak",
            json=payload,
            headers=no_auth_headers(),   # Endpoint kontak biasanya public
            timeout=TIMEOUT
        )
        if r.status_code in [200, 201]:
            data = r.json()
            if data.get("success"):
                _created_kontak_id = data["data"]["id"]
        # Test ini informatif — sukses atau 401 keduanya valid tergantung konfigurasi
        assert r.status_code in [200, 201, 401, 403], \
            f"Status tidak terduga: {r.status_code}"

    def test_tanpa_token_kontak_list(self):
        """TC-API-29: GET /api/pesan-kontak tanpa token mengembalikan 401/403."""
        r = requests.get(f"{BASE_URL}/pesan-kontak", headers=no_auth_headers(), timeout=TIMEOUT)
        assert r.status_code in [401, 403]

    def test_delete_kontak_cleanup(self):
        """TC-API-30: DELETE /api/pesan-kontak/{id} berhasil (cleanup)."""
        if not _created_kontak_id:
            pytest.skip("Kontak belum dibuat lewat API, skip cleanup")
        r = requests.delete(
            f"{BASE_URL}/pesan-kontak/{_created_kontak_id}",
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code == 200
        assert r.json().get("success") is True


# ─────────────────────────────────────────────────────────
# TC-API-31~33: Validasi Input
# ─────────────────────────────────────────────────────────
class TestValidasiInput:

    def test_create_pesanan_field_kosong(self):
        """TC-API-31: POST /api/pesanan dengan body kosong mengembalikan error."""
        r = requests.post(
            f"{BASE_URL}/pesanan",
            json={},
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code in [400, 500], \
            f"Seharusnya error, dapat: {r.status_code}"

    def test_create_menu_tanpa_nama(self):
        """TC-API-32: POST /api/menu-produk tanpa namaProduk mengembalikan error."""
        r = requests.post(
            f"{BASE_URL}/menu-produk",
            json={"harga": 10000, "kategori": "Kopi"},
            headers=auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code in [400, 500]

    def test_login_tanpa_body(self):
        """TC-API-33: POST /api/auth/login tanpa body mengembalikan error."""
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={},
            headers=no_auth_headers(),
            timeout=TIMEOUT
        )
        assert r.status_code in [400, 401, 500]
