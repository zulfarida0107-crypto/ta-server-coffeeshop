-- =========================================================
-- Database: ta_db_coffeeshop
-- =========================================================

-- 1. Tabel User (Standalone)
CREATE TABLE `user` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `nama_lengkap` VARCHAR(255) NOT NULL,
  `role` VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 2. Tabel Pesan Kontak (Standalone)
CREATE TABLE `pesan_kontak` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nama` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `subjek` VARCHAR(255) NOT NULL,
  `pesan` TEXT NOT NULL,
  `tanggal_dikirim` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. Tabel Menu Produk (Master Data)
CREATE TABLE `menu_produk` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nama_produk` VARCHAR(255) NOT NULL,
  `harga` DECIMAL(10,2) NOT NULL,
  `deskripsi` TEXT,
  `kategori` VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- 4. Tabel Pesanan (Berelasi dengan Menu Produk)
CREATE TABLE `pesanan` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nama_pelanggan` VARCHAR(255) NOT NULL,
  `id_produk` INT NOT NULL,
  `jumlah` INT NOT NULL,
  `total_harga` DECIMAL(10,2) NOT NULL,
  `status_pesanan` VARCHAR(50) NOT NULL,
  `tanggal_pesanan` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `detail_pesanan` TEXT,
  CONSTRAINT `fk_pesanan_produk` FOREIGN KEY (`id_produk`) REFERENCES `menu_produk`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 5. Tabel Desain Pesanan (Berelasi dengan Pesanan)
CREATE TABLE `desain_pesanan` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `id_pesanan` INT NOT NULL,
  `file_desain_url` TEXT,
  `keterangan` TEXT,
  `tanggal_upload` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `status_pesanan` VARCHAR(50) NOT NULL DEFAULT 'Baru',
  CONSTRAINT `fk_desain_pesanan` FOREIGN KEY (`id_pesanan`) REFERENCES `pesanan`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================================================
-- SEED DATA
-- =========================================================

-- Seed Users
INSERT INTO `user` (id, username, password, nama_lengkap, role) VALUES 
(1, 'admin', 'admin123', 'Administrator Toko', 'Admin'),
(2, 'karyawan', 'karyawan123', 'Karyawan Coffee Shop', 'Karyawan')
ON DUPLICATE KEY UPDATE username=VALUES(username);

-- Seed Menu & Produk
INSERT INTO `menu_produk` (id, nama_produk, harga, deskripsi, kategori, bagian, gambar) VALUES 
(1, 'Espresso', 15000, 'Kopi hitam murni pekat diekstrak dengan tekanan tinggi', 'Kopi', 'Menu Kami', '1.jpg'),
(2, 'Cappuccino', 25000, 'Kopi dengan perpaduan espresso, susu pemanas, dan busa susu tebal', 'Kopi', 'Menu Kami', '2.jpg'),
(3, 'Latte', 28000, 'Espresso dicampur susu dengan lapisan busa susu yang tipis', 'Kopi', 'Menu Kami', '3.jpg'),
(4, 'Americano', 18000, 'Espresso dicampur air hangat untuk rasa yang lebih ringan', 'Kopi', 'Menu Kami', '4.jpg'),
(5, 'Mocha', 30000, 'Espresso dengan tambahan cokelat lezat dan susu hangat', 'Kopi', 'Menu Kami', '5.jpg'),
(6, 'Macchiato', 20000, 'Espresso dengan sedikit busa susu hangat di atasnya', 'Kopi', 'Menu Kami', '6.jpg'),
(7, 'Matcha Latte', 26000, 'Susu creamy berpadu dengan bubuk teh hijau Jepang premium', 'Non-Kopi', 'Produk Unggulan', '7.jpg'),
(8, 'Chocolate', 24000, 'Minuman cokelat creamy dengan rasa manis alami', 'Non-Kopi', 'Produk Unggulan', '8.jpg'),
(9, 'Croissant', 22000, 'Roti panggang mentega berlapis khas Prancis yang renyah', 'Pastry', 'Produk Unggulan', '9.jpg'),
(10, 'Chocolate Danish', 24000, 'Pastry renyah dengan isian cokelat manis di dalamnya', 'Pastry', 'Produk Unggulan', '10.jpg'),
(11, 'Kopi Aceh Gayo', 35000, 'Di daerah paling barat di Indonesia, terdapat dua jenis kopi yang diproduksi, yaitu kopi jenis Arabika dan Robusta. Nah, yang paling terkenal dari Aceh adalah kopi Gayo Arabika-nya yang digadang-gadang sebagai salah satu kopi terbaik di dunia. Karakteristik yang paling kuat milik kopi Aceh Gayo ini adalah aromanya yang sangat tajam. Selain itu, kopi Gayo tidak memberi bekas rasa pahit yang lekat di lidah setelah meminumnya, berbeda dengan kebanyakan jenis kopi di Indonesia lainnya yang meninggalkan aftertaste pahit. Inilah alasan mengapa banyak orang sangat menikmati kopi Aceh Gayo.', 'Kopi', 'Produk Unggulan', 'aceh_gayo.jpg'),
(12, 'Kopi Lampung', 28000, 'Berbeda dengan Aceh Gayo yang lebih terkenal dengan jenis kopi Arabikanya, kopi Lampung justru sangat mengunggulkan kopi jenis Robusta. Karakteristik yang sangat terasa dari kopi nusantara asal Lampung teksturnya yang halus, namun rasanya yang cukup kuat. Metode dry processing yang digunakan dalam pengolahan biji kopi Lampung ini pun diyakini sebagai asal mula cita rasa dan karakteristik yang kuat di dalamnya.', 'Kopi', 'Produk Unggulan', 'lampung.jpg'),
(13, 'Kopi Toraja', 32000, 'Memiliki nama lain Celebes Kalossi, kopi asal daerah Sulawesi ini memiliki aroma yang sangat khas juga harum. Yang membuatnya cukup disukai adalah tingkat keasaman yang rendah. Keunikan dari karakteristik kopi Toraja terdapat pada kecenderungan rasa floral and fruity yang dihasilkan. Selain itu, rasa kopinya yang kuat dan sedikit kecut meninggalkan aftertaste yang unik di lidah.', 'Kopi', 'Produk Unggulan', 'toraja.jpg'),
(14, 'Kopi Jawa', 25000, 'Produksi biji kopi Jawa umumnya dilakukan dengan metode wet processing sehingga cita rasanya mungkin sedikit berbeda dan tidak sekuat biji kopi yang dihasilkan di Sumatera atau Sulawesi. Meskipun begitu, jenis kopi Arabika ini sangat dinikmati karena rasanya yang dinilai \'seimbang\'. Tingkat keasaman yang medium dan kekentalan yang nggak terlalu pekat menjadi serta semilir aroma rempah yang dihasilkan, membuat ciri khas sendiri saat menenggaknya.', 'Kopi', 'Produk Unggulan', 'jawa.jpg'),
(15, 'Kopi Bali Kintamani', 30000, 'Karakteristik kopi nusantara yang satu ini adalah cita rasa kesegaran dari asam (citrus) seperti jeruk. Aromanya dianggap eksotis dilengkapi dengan tekstur yang light, membuat kopi ini tidak terlalu terasa pahit dan tidak meninggalkan aftertaste pekat setelahnya. Nah, oleh sebab itu, kopi jenis ini mungkin saja bisa lebih banyak dinikmati oleh orang-orang yang tidak terlalu suka minum kopi dengan body yang \'berat\'.', 'Kopi', 'Produk Unggulan', 'bali.jpg'),
(16, 'Kopi Flores Bajawa', 34000, 'Kopi Arabika asal Flores Bajawa ini menghasilkan tingkat keasaman medium serta tekstur rasa yang ringan. Selain dari aromanya yang menggiurkan, karakteristik kopi ini juga dikenal dengan sensasi manis juga cita rasa kacang-kacangan dan herbal di dalamnya. Keunikan ini yang bisa jadi tidak bisa kamu nikmati pada kopi-kopi lainnya. Nggak heran kalau jenis Flores Bajawa ini bisa menembus pasar internasional karena keunggulan tersebut, kan?', 'Kopi', 'Produk Unggulan', 'flores.jpg'),
(17, 'Kopi Papua Wamena', 38000, 'Ketajaman aroma dengan cita rasa yang ringan merupakan ciri khas dari kopi nusantara dari bagian timur Indonesia ini. Mirip kopi Bali yang memiliki rasa floral, kopi Papua Wamena juga dilengkapi dengan nuansa harum coklat dan herbal. Aftertaste \'smokey\' setelah meminumnya pun menjadi ciri khas dan keunikan tersendiri. Teksturnya yang lembut dan tidak berampas juga sangat ramah di mulut.', 'Kopi', 'Produk Unggulan', 'papua.jpg')
ON DUPLICATE KEY UPDATE nama_produk=VALUES(nama_produk), harga=VALUES(harga), deskripsi=VALUES(deskripsi), kategori=VALUES(kategori), bagian=VALUES(bagian), gambar=VALUES(gambar);

