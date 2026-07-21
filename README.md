# Classic Coffee Server Backend

Classic Coffee Server Backend — A secure and high-performance Spring Boot REST API serving as the central coordinator for user management, ordering, custom product design review, and database integration.

## Fitur Utama

- **RESTful API Service:** Endpoint lengkap untuk manajemen pengguna, data produk menu, pengelolaan pesanan pelanggan, serta review kue custom.
- **ORM & Database Integration:** Menggunakan Spring Data JPA (Hibernate) untuk komunikasi data yang cepat dan aman dengan MySQL.
- **Relational Integrity:** Validasi Foreign Key dan integritas relasi antar tabel (user, menu_produk, pesanan, dan desain_pesanan).
- **CORS & Security:** Konfigurasi keamanan CORS untuk melayani request dari CodeIgniter 4 Web dan Flutter Client secara bersamaan.

## Keterangan Operasi CRUD

Server backend Spring Boot ini menyediakan antarmuka API RESTful lengkap yang mengelola operasi CRUD (Create, Read, Update, Delete) pada database MySQL untuk entitas berikut:

1. **Entitas User (`/api/users`):**
   - **Create:** Menambahkan user/administrator baru melalui request `POST /api/users`.
   - **Read:** Mengambil daftar seluruh user (`GET /api/users`) atau user spesifik berdasarkan ID (`GET /api/users/{id}`).
   - **Update:** Memperbarui informasi akun user (`PUT /api/users/{id}`).
   - **Delete:** Menghapus akun user dari database (`DELETE /api/users/{id}`).
2. **Entitas Menu Produk (`/api/menu-produk`):**
   - **Create:** Menambahkan item menu kopi atau kue baru via `POST /api/menu-produk`.
   - **Read:** Mendapatkan semua menu (`GET /api/menu-produk`) atau menu tertentu berdasarkan ID (`GET /api/menu-produk/{id}`).
   - **Update:** Memperbarui nama, harga, deskripsi, atau kategori menu (`PUT /api/menu-produk/{id}`).
   - **Delete:** Menghapus item menu dari database (`DELETE /api/menu-produk/{id}`).
3. **Entitas Pesanan (`/api/pesanan`):**
   - **Create:** Membuat pesanan pelanggan baru (`POST /api/pesanan`).
   - **Read:** Mendapatkan daftar seluruh antrean pesanan (`GET /api/pesanan`) atau pesanan spesifik (`GET /api/pesanan/{id}`).
   - **Update:** Mengubah status pengerjaan pesanan dan status pembayaran (`PUT /api/pesanan/{id}`).
   - **Delete:** Membatalkan/menghapus pesanan dari sistem (`DELETE /api/pesanan/{id}`).
4. **Entitas Desain Pesanan / Kue Custom (`/api/desain-pesanan`):**
   - **Create:** Menyimpan pengiriman desain kue custom pelanggan (`POST /api/desain-pesanan`).
   - **Read:** Mendapatkan seluruh kiriman desain kue (`GET /api/desain-pesanan`) atau desain spesifik (`GET /api/desain-pesanan/{id}`).
   - **Update:** Memperbarui catatan pengerjaan atau status desain kue (`PUT /api/desain-pesanan/{id}`).
   - **Delete:** Menghapus pesanan kue custom (`DELETE /api/desain-pesanan/{id}`).
5. **Entitas Pesan Kontak (`/api/pesan-kontak`):**
   - **Create:** Menerima pesan masukan/formulir kontak pelanggan (`POST /api/pesan-kontak`).
   - **Read:** Menampilkan kotak masuk pesan pelanggan (`GET /api/pesan-kontak`).
   - **Update:** Mengubah status pembacaan atau balasan pesan (`PUT /api/pesan-kontak/{id}`).
   - **Delete:** Menghapus pesan masuk dari sistem (`DELETE /api/pesan-kontak/{id}`).

## Teknologi

- **Framework:** Spring Boot (Java)
- **Database Connector:** Spring Data JPA, Hibernate
- **Database:** MySQL
- **Build Tool:** Maven

## Panduan Instalasi & Menjalankan Project

1. Pastikan Java Development Kit (JDK) versi 17+ telah terinstal di komputer Anda.
2. Buat database MySQL baru bernama `db_coffeeshop` (atau sesuaikan dengan file `application.properties`).
3. Clone repository ini ke direktori lokal Anda.
4. Sesuaikan konfigurasi username dan password database MySQL Anda di file `src/main/resources/application.properties`.
5. Jalankan server lokal melalui Maven Wrapper:
   ```bash
   # Windows (PowerShell)
   .\mvnw.cmd spring-boot:run
   
   # Linux/macOS
   ./mvnw spring-boot:run
   ```
6. Server backend akan aktif di alamat `http://localhost:8083`.

## Deployment / Publikasi via GitHub

Untuk mempublikasikan server backend Spring Boot secara online, Anda dapat menghubungkan repository GitHub Anda ke penyedia layanan cloud (seperti Render, Railway, Heroku, AWS, atau VPS):

### Opsi 1: Integrasi Cloud Deployment (Render / Railway)
1. Buat akun pada platform cloud deployment pilihan Anda (misalnya Render atau Railway).
2. Hubungkan akun cloud tersebut dengan akun GitHub Anda.
3. Buat layanan baru (Web Service) dan pilih repository `ta-server-coffeeshop` Anda.
4. Tentukan perintah build dan start untuk Maven Spring Boot:
   - Build Command: `./mvnw clean package -DskipTests`
   - Start Command: `java -jar target/your-app-name-0.0.1-SNAPSHOT.jar` (sesuaikan nama file jar hasil build)
5. Tambahkan variabel environment untuk koneksi database MySQL online (seperti url host, username, dan password database) pada panel konfigurasi cloud Anda.

### Opsi 2: Docker Containerization
Anda dapat menambahkan file `Dockerfile` pada root repository untuk membungkus server backend Spring Boot ke dalam container Docker, mempermudah deployment ke VPS atau Google Cloud Run.

---

## Dokumentasi & Demo

Gunakan kolom di bawah ini untuk menambahkan tangkapan layar (screenshot), animasi GIF, atau video dokumentasi aplikasi Anda.

| Fitur | Tampilan Dokumentasi | Deskripsi |
| --- | --- | --- |
| **Endpoint Swagger / API Docs** | ![Postman 1](documentation/postman_api_docs_1.png) <br> ![Postman 2](documentation/postman_api_docs_2.png) <br> ![Postman 3](documentation/postman_api_docs_3.png) | Dokumentasi pengetesan endpoint REST API (User, Menu, Pesanan, Desain Custom, Kontak) menggunakan Postman. |
| **Koneksi Database MySQL** | ![Database HeidiSQL](documentation/database_heidisql.png) | Struktur tabel database `ta_db_coffeeshop` pada HeidiSQL: desain_pesanan, menu_produk, pesanan, pesan_kontak, user. |
| **Log Aktivitas Server** | *(Masukkan gambar di sini)* | Tampilan log konsol saat server Spring Boot menerima request transaksi. |
| **Cuplikan Kode Proteksi Endpoint (SecurityConfig)** | ![Security Config](documentation/snippet_security_config.png) | Logika filter keamanan berlapis JWT Spring Boot: endpoint publik CI4 & endpoint privat Flutter Dashboard. |
