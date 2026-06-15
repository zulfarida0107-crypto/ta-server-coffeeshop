package com.coffeeshop.server.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "desain_pesanan")
public class DesainPesanan {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "id_pesanan", nullable = false)
    private Long idPesanan;

    @Column(name = "file_desain_url", columnDefinition = "TEXT")
    private String fileDesainUrl;

    @Column(columnDefinition = "TEXT")
    private String keterangan;

    @Column(name = "tanggal_upload")
    private String tanggalUpload;

    @Column(name = "status_pesanan", nullable = false)
    private String statusPesanan = "Baru";
}
