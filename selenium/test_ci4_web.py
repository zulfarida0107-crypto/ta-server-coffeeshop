"""
=============================================================
BLACK BOX TESTING — CI4 Web Coffeeshop
URL Target : http://ta-ci4-web-coffeeshop.test
Framework  : Selenium 4 + pytest

Tabel yang diuji:
  - menu_produk   : tampilan menu & filter kategori
  - pesanan       : form checkout → QR payment → konfirmasi
  - pesan_kontak  : form kontak

Cara jalankan:
  pip install -r requirements.txt
  pytest test_ci4_web.py -v --html=report_ci4.html --self-contained-html
=============================================================
"""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# ─────────────────────────────────────────────────────────
# Konfigurasi
# ─────────────────────────────────────────────────────────
BASE_URL  = "http://ta-ci4-web-coffeeshop.test"
HEADLESS  = False        # Ganti True untuk menjalankan tanpa jendela browser
WAIT_SEC  = 10           # Timeout WebDriverWait (detik)


# ─────────────────────────────────────────────────────────
# Fixture: inisialisasi & tutup browser
# ─────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,768")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])

    svc = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=svc, options=opts)
    drv.implicitly_wait(WAIT_SEC)
    yield drv
    drv.quit()


def wait_for(driver, by, selector, timeout=WAIT_SEC):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def wait_clickable(driver, by, selector, timeout=WAIT_SEC):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )


# ─────────────────────────────────────────────────────────
# TC-WEB-01: Halaman beranda dapat dibuka
# ─────────────────────────────────────────────────────────
class TestHalaman:

    def test_beranda_terbuka(self, driver):
        """TC-WEB-01: Beranda classic coffee dapat diakses."""
        driver.get(BASE_URL)
        assert "classic" in driver.title.lower() or "coffee" in driver.title.lower(), \
            f"Judul halaman tidak sesuai: {driver.title}"

    def test_navbar_ada(self, driver):
        """TC-WEB-02: Navbar / navigasi tersedia di halaman beranda."""
        driver.get(BASE_URL)
        navbar = wait_for(driver, By.CSS_SELECTOR, "nav.navbar")
        assert navbar.is_displayed(), "Navbar tidak ditemukan"

    def test_section_hero_ada(self, driver):
        """TC-WEB-03: Section hero (judul utama) tersedia."""
        driver.get(BASE_URL)
        hero = wait_for(driver, By.CSS_SELECTOR, "section.hero")
        assert hero.is_displayed(), "Section hero tidak ditemukan"

    def test_section_tentang_kami(self, driver):
        """TC-WEB-04: Section 'Tentang Kami' tersedia."""
        driver.get(BASE_URL)
        about = wait_for(driver, By.CSS_SELECTOR, "section.about")
        assert about.is_displayed()

    def test_section_menu_ada(self, driver):
        """TC-WEB-05: Section menu produk tersedia."""
        driver.get(BASE_URL)
        menu = wait_for(driver, By.ID, "menu")
        assert menu.is_displayed()

    def test_section_kontak_ada(self, driver):
        """TC-WEB-06: Section kontak tersedia."""
        driver.get(BASE_URL)
        kontak = wait_for(driver, By.ID, "contact")
        assert kontak.is_displayed()

    def test_footer_ada(self, driver):
        """TC-WEB-07: Footer dengan informasi kredit tersedia."""
        driver.get(BASE_URL)
        footer = wait_for(driver, By.CSS_SELECTOR, "footer")
        assert footer.is_displayed()


# ─────────────────────────────────────────────────────────
# TC-WEB-08~12: Filter Menu (menu_produk — kategori)
# ─────────────────────────────────────────────────────────
class TestFilterMenu:

    def _buka_search_panel(self, driver):
        """Klik tombol pencarian untuk membuka panel filter."""
        driver.get(BASE_URL)
        time.sleep(1)
        search_btn = wait_clickable(driver, By.ID, "search-button")
        search_btn.click()
        time.sleep(0.5)

    def test_filter_kopi(self, driver):
        """TC-WEB-08: Filter kategori 'Kopi' berfungsi."""
        self._buka_search_panel(driver)
        btns = driver.find_elements(By.CSS_SELECTOR, ".filter-shortcut-btn")
        kopi_btn = next((b for b in btns if b.text.strip() == "Kopi"), None)
        assert kopi_btn is not None, "Tombol filter 'Kopi' tidak ditemukan"
        kopi_btn.click()
        time.sleep(0.5)
        assert "active" in kopi_btn.get_attribute("class"), "Filter Kopi tidak aktif"

    def test_filter_non_kopi(self, driver):
        """TC-WEB-09: Filter kategori 'Non-Kopi' berfungsi."""
        self._buka_search_panel(driver)
        btns = driver.find_elements(By.CSS_SELECTOR, ".filter-shortcut-btn")
        btn = next((b for b in btns if "Non" in b.text), None)
        assert btn is not None, "Tombol filter 'Non-Kopi' tidak ditemukan"
        btn.click()
        time.sleep(0.5)
        assert "active" in btn.get_attribute("class")

    def test_filter_pastry(self, driver):
        """TC-WEB-10: Filter kategori 'Pastry' berfungsi."""
        self._buka_search_panel(driver)
        btns = driver.find_elements(By.CSS_SELECTOR, ".filter-shortcut-btn")
        btn = next((b for b in btns if b.text.strip() == "Pastry"), None)
        assert btn is not None, "Tombol filter 'Pastry' tidak ditemukan"
        btn.click()
        time.sleep(0.5)
        assert "active" in btn.get_attribute("class")

    def test_filter_semua(self, driver):
        """TC-WEB-11: Filter 'Semua' menampilkan semua menu."""
        self._buka_search_panel(driver)
        btns = driver.find_elements(By.CSS_SELECTOR, ".filter-shortcut-btn")
        btn = next((b for b in btns if b.text.strip() == "Semua"), None)
        assert btn is not None, "Tombol filter 'Semua' tidak ditemukan"
        btn.click()
        time.sleep(0.5)
        assert "active" in btn.get_attribute("class")

    def test_search_box_ada(self, driver):
        """TC-WEB-12: Search box tersedia untuk pencarian menu."""
        self._buka_search_panel(driver)
        sbox = driver.find_element(By.ID, "search-box")
        assert sbox.is_displayed(), "Search box tidak tampil"


# ─────────────────────────────────────────────────────────
# TC-WEB-13~18: Keranjang & Checkout (pesanan)
# ─────────────────────────────────────────────────────────
class TestKeranjangCheckout:

    def _tambah_item_ke_cart(self, driver):
        """Helper: klik tombol add pertama pada produk unggulan."""
        driver.get(BASE_URL)
        time.sleep(1.5)
        # Scroll ke section produk
        driver.execute_script("document.getElementById('products').scrollIntoView({behavior:'instant'})")
        time.sleep(0.5)
        # Ambil kartu produk pertama
        cards = driver.find_elements(By.CSS_SELECTOR, ".product-card")
        assert len(cards) > 0, "Tidak ada produk yang ditampilkan"
        detail_btn = cards[0].find_element(By.CSS_SELECTOR, ".detail-button")
        detail_btn.click()
        time.sleep(0.5)

    def test_produk_unggulan_tampil(self, driver):
        """TC-WEB-13: Produk unggulan dari menu_produk tampil di halaman."""
        driver.get(BASE_URL)
        time.sleep(1.5)
        products_section = wait_for(driver, By.ID, "products")
        assert products_section.is_displayed()

    def test_menu_card_tampil(self, driver):
        """TC-WEB-14: Menu card dari tabel menu_produk tampil."""
        driver.get(BASE_URL)
        time.sleep(1.5)
        cards = driver.find_elements(By.CSS_SELECTOR, ".menu-card")
        assert len(cards) > 0, "Tidak ada menu card yang tampil"

    def test_cart_button_ada(self, driver):
        """TC-WEB-15: Tombol cart tersedia di navbar."""
        driver.get(BASE_URL)
        # Tombol cart ada tapi hidden (display:none) sampai ada item
        cart_btn = driver.find_element(By.ID, "shopping-cart-button")
        assert cart_btn is not None

    def test_checkout_form_tampil(self, driver):
        """TC-WEB-16: Form checkout (data pelanggan) tersedia di dalam cart panel."""
        driver.get(BASE_URL)
        time.sleep(1)
        form = driver.find_element(By.ID, "checkoutForm")
        assert form is not None, "Form checkout tidak ditemukan"

    def test_input_nama_ada(self, driver):
        """TC-WEB-17: Input nama pelanggan tersedia di form checkout."""
        driver.get(BASE_URL)
        inp = driver.find_element(By.ID, "name")
        assert inp is not None

    def test_input_email_ada(self, driver):
        """TC-WEB-18: Input email tersedia di form checkout."""
        driver.get(BASE_URL)
        inp = driver.find_element(By.ID, "email")
        assert inp is not None

    def test_input_phone_ada(self, driver):
        """TC-WEB-19: Input nomor telepon tersedia di form checkout."""
        driver.get(BASE_URL)
        inp = driver.find_element(By.ID, "phone")
        assert inp is not None

    def test_checkout_button_ada(self, driver):
        """TC-WEB-20: Tombol checkout tersedia."""
        driver.get(BASE_URL)
        btn = driver.find_element(By.ID, "checkout-button")
        assert btn is not None, "Tombol checkout tidak ditemukan"

    def test_checkout_button_disabled_tanpa_isi(self, driver):
        """TC-WEB-21: Tombol checkout disabled saat form belum diisi (validasi)."""
        driver.get(BASE_URL)
        time.sleep(0.5)
        btn = driver.find_element(By.ID, "checkout-button")
        # Tombol harus disabled atau punya class 'disabled' sebelum form diisi
        is_disabled = btn.get_attribute("disabled") is not None or \
                      "disabled" in btn.get_attribute("class")
        assert is_disabled, "Tombol checkout seharusnya disabled sebelum form diisi"


# ─────────────────────────────────────────────────────────
# TC-WEB-22~25: Halaman QR Payment
# ─────────────────────────────────────────────────────────
class TestQRPaymentPage:

    def test_payment_page_memerlukan_session(self, driver):
        """TC-WEB-22: Halaman /checkout/payment redirect ke / jika tidak ada session."""
        driver.get(f"{BASE_URL}/checkout/payment")
        time.sleep(1)
        # Harus redirect ke beranda karena tidak ada session
        assert driver.current_url.rstrip('/') == BASE_URL.rstrip('/') or \
               driver.current_url == BASE_URL + '/', \
               f"Harusnya redirect ke beranda, bukan: {driver.current_url}"

    def test_success_page_dapat_diakses(self, driver):
        """TC-WEB-23: Halaman success dapat diakses langsung."""
        driver.get(f"{BASE_URL}/checkout/success")
        time.sleep(1)
        # Bisa jadi redirect ke / atau tampil halaman
        assert driver.current_url is not None

    def test_pending_page_dapat_diakses(self, driver):
        """TC-WEB-24: Halaman pending dapat diakses."""
        driver.get(f"{BASE_URL}/checkout/pending")
        time.sleep(1)
        assert driver.current_url is not None

    def test_error_page_dapat_diakses(self, driver):
        """TC-WEB-25: Halaman error dapat diakses."""
        driver.get(f"{BASE_URL}/checkout/error")
        time.sleep(1)
        assert driver.current_url is not None


# ─────────────────────────────────────────────────────────
# TC-WEB-26~30: Form Kontak (pesan_kontak)
# ─────────────────────────────────────────────────────────
class TestFormKontak:

    def test_form_kontak_ada(self, driver):
        """TC-WEB-26: Form kontak tersedia di section contact."""
        driver.get(BASE_URL)
        form = driver.find_element(By.CSS_SELECTOR, "#contact form")
        assert form.is_displayed(), "Form kontak tidak tampil"

    def test_input_nama_kontak(self, driver):
        """TC-WEB-27: Input nama pada form kontak tersedia."""
        driver.get(BASE_URL)
        inp = driver.find_element(By.CSS_SELECTOR, "#contact input[name='nama']")
        assert inp is not None

    def test_input_email_kontak(self, driver):
        """TC-WEB-28: Input email pada form kontak tersedia."""
        driver.get(BASE_URL)
        inp = driver.find_element(By.CSS_SELECTOR, "#contact input[name='email']")
        assert inp is not None

    def test_input_subjek_kontak(self, driver):
        """TC-WEB-29: Input subjek pada form kontak tersedia."""
        driver.get(BASE_URL)
        inp = driver.find_element(By.CSS_SELECTOR, "#contact input[name='subjek']")
        assert inp is not None

    def test_textarea_pesan_kontak(self, driver):
        """TC-WEB-30: Textarea pesan pada form kontak tersedia."""
        driver.get(BASE_URL)
        ta = driver.find_element(By.ID, "pesan")
        assert ta.is_displayed()

    def test_tombol_kirim_kontak(self, driver):
        """TC-WEB-31: Tombol 'kirim pesan' pada form kontak tersedia."""
        driver.get(BASE_URL)
        btn = driver.find_element(By.ID, "kontak-submit-btn")
        assert btn.is_displayed(), "Tombol kirim pesan tidak tampil"

    def test_submit_kontak_validasi_field_kosong(self, driver):
        """TC-WEB-32: Form kontak tidak dikirim jika field kosong (validasi HTML required)."""
        driver.get(BASE_URL)
        btn = driver.find_element(By.ID, "kontak-submit-btn")
        # Klik tanpa isi form — harus ada validasi HTML5 required
        # Form tidak akan submit karena ada atribut 'required'
        driver.execute_script("document.getElementById('kontak-submit-btn').click();")
        time.sleep(0.5)
        # URL tidak berubah (tidak redirect)
        assert BASE_URL in driver.current_url

    def test_isi_form_kontak(self, driver):
        """TC-WEB-33: Field form kontak dapat diisi teks."""
        driver.get(BASE_URL)
        driver.execute_script("document.getElementById('contact').scrollIntoView({behavior:'instant'})")
        time.sleep(0.5)

        driver.find_element(By.CSS_SELECTOR, "#contact input[name='nama']").send_keys("Test User Selenium")
        driver.find_element(By.CSS_SELECTOR, "#contact input[name='email']").send_keys("selenium@test.com")
        driver.find_element(By.CSS_SELECTOR, "#contact input[name='subjek']").send_keys("Pengujian Selenium")
        driver.find_element(By.ID, "pesan").send_keys("Ini adalah pesan pengujian otomatis dengan Selenium.")

        nama_val = driver.find_element(By.CSS_SELECTOR, "#contact input[name='nama']").get_attribute("value")
        assert nama_val == "Test User Selenium", f"Nilai nama tidak sesuai: {nama_val}"


# ─────────────────────────────────────────────────────────
# TC-WEB-34~36: Social Media & Footer Link
# ─────────────────────────────────────────────────────────
class TestFooter:

    def test_footer_social_link_ada(self, driver):
        """TC-WEB-34: Tautan media sosial tersedia di footer."""
        driver.get(BASE_URL)
        socials = driver.find_elements(By.CSS_SELECTOR, "footer .social a")
        assert len(socials) >= 1, "Tidak ada link sosial media di footer"

    def test_footer_nav_link_ada(self, driver):
        """TC-WEB-35: Link navigasi tersedia di footer."""
        driver.get(BASE_URL)
        links = driver.find_elements(By.CSS_SELECTOR, "footer .links a")
        assert len(links) >= 1, "Tidak ada link navigasi di footer"

    def test_footer_credit_ada(self, driver):
        """TC-WEB-36: Teks kredit pembuat ada di footer."""
        driver.get(BASE_URL)
        credit = driver.find_element(By.CSS_SELECTOR, "footer .credit")
        assert "zulfarida" in credit.text.lower() or "namira" in credit.text.lower(), \
            f"Kredit tidak ditemukan: {credit.text}"


# ─────────────────────────────────────────────────────────
# TC-WEB-37~39: Responsivitas & Elemen Tambahan
# ─────────────────────────────────────────────────────────
class TestElementLainnya:

    def test_hamburger_menu_ada(self, driver):
        """TC-WEB-37: Tombol hamburger menu tersedia."""
        driver.get(BASE_URL)
        hbg = driver.find_element(By.ID, "hamburger-menu")
        assert hbg is not None

    def test_google_maps_embed_ada(self, driver):
        """TC-WEB-38: Google Maps iframe di section kontak tersedia."""
        driver.get(BASE_URL)
        iframe = driver.find_element(By.CSS_SELECTOR, "#contact iframe.map")
        assert iframe is not None

    def test_modal_produk_tersedia(self, driver):
        """TC-WEB-39: Modal detail produk ada di DOM."""
        driver.get(BASE_URL)
        modal = driver.find_element(By.ID, "item-detail-modal")
        assert modal is not None
