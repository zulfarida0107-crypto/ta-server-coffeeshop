# Classic Coffee Server Backend

Classic Coffee Server Backend — A secure and high-performance Spring Boot REST API serving as the central coordinator for user management, ordering, custom product design review, and database integration.

## Fitur Utama

- **RESTful API Service:** Endpoint lengkap untuk manajemen pengguna, data produk menu, pengelolaan pesanan pelanggan, serta review kue custom.
- **ORM & Database Integration:** Menggunakan Spring Data JPA (Hibernate) untuk komunikasi data yang cepat dan aman dengan MySQL.
- **Relational Integrity:** Validasi Foreign Key dan integritas relasi antar tabel (user, menu_produk, pesanan, dan desain_pesanan).
- **CORS & Security:** Konfigurasi keamanan CORS untuk melayani request dari CodeIgniter 4 Web dan Flutter Client secara bersamaan.

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

---

## Dokumentasi & Demo

Gunakan kolom di bawah ini untuk menambahkan tangkapan layar (screenshot), animasi GIF, atau video dokumentasi aplikasi Anda.

| Fitur | Tampilan Dokumentasi | Deskripsi |
| --- | --- | --- |
| **Endpoint Swagger / API Docs** | *(Masukkan gambar di sini)* | Dokumentasi endpoint REST API yang tersedia pada server backend. |
| **Koneksi Database MySQL** | *(Masukkan gambar di sini)* | Struktur tabel database `db_coffeeshop` pada phpMyAdmin / DBeaver. |
| **Log Aktivitas Server** | *(Masukkan gambar di sini)* | Tampilan log konsol saat server Spring Boot menerima request transaksi. |
