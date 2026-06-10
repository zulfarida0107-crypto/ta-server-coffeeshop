package com.coffeeshop.server.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "menu_produk")
public class MenuProduk {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "nama_produk", nullable = false)
    private String namaProduk;

    @Column(nullable = false)
    private Double harga;

    @Column(columnDefinition = "TEXT")
    private String deskripsi;

    @Column(nullable = false)
    private String kategori;
}
