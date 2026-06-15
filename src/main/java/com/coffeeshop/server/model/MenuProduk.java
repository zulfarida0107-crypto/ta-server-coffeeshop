package com.coffeeshop.server.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "menu_produk")
public class MenuProduk {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // Menggunakan Long untuk ID adalah standar yang bagus di Spring Boot

    @Column(name = "nama_produk", nullable = false)
    private String namaProduk;

    @Column(nullable = false)
    private Integer harga; // <-- Tipe data diubah menjadi Integer agar sinkron dengan INT di MySQL

    @Column(columnDefinition = "TEXT")
    private String deskripsi;

    @Column(nullable = false)
    private String kategori;
}