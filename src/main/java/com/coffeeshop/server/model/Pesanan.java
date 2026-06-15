package com.coffeeshop.server.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "pesanan")
public class Pesanan {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "nama_pelanggan", nullable = false)
    private String namaPelanggan;

    @Column(name = "id_produk", nullable = false)
    private Long idProduk;

    @Column(nullable = false)
    private Integer jumlah;

    @Column(name = "total_harga", nullable = false)
    private Double totalHarga;

    @Column(name = "status_pesanan", nullable = false)
    private String statusPesanan = "Baru";

    @Column(name = "tanggal_pesanan")
    private String tanggalPesanan;

    @Column(name = "detail_pesanan", columnDefinition = "TEXT")
    private String detailPesanan;
}
