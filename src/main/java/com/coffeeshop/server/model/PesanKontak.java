package com.coffeeshop.server.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "pesan_kontak")
public class PesanKontak {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nama;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String subjek;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String pesan;

    @Column(name = "tanggal_dikirim")
    private String tanggalDikirim;
}
