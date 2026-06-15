package com.coffeeshop.server.service;

import com.coffeeshop.server.model.Pesanan;
import com.coffeeshop.server.repository.PesananRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PesananService {

    @Autowired
    private PesananRepository repository;

    public List<Pesanan> findAll() {
        return repository.findAll();
    }

    public Optional<Pesanan> findById(Long id) {
        return repository.findById(id);
    }

    public Pesanan save(Pesanan pesanan) {
        if (pesanan.getStatusPesanan() == null || pesanan.getStatusPesanan().trim().isEmpty()) {
            pesanan.setStatusPesanan("Baru");
        }
        return repository.save(pesanan);
    }

    public Optional<Pesanan> update(Long id, Pesanan pesananDetails) {
        return repository.findById(id).map(pesanan -> {
            pesanan.setNamaPelanggan(pesananDetails.getNamaPelanggan());
            pesanan.setIdProduk(pesananDetails.getIdProduk());
            pesanan.setJumlah(pesananDetails.getJumlah());
            pesanan.setTotalHarga(pesananDetails.getTotalHarga());
            pesanan.setStatusPesanan(pesananDetails.getStatusPesanan());
            pesanan.setTanggalPesanan(pesananDetails.getTanggalPesanan());
            pesanan.setDetailPesanan(pesananDetails.getDetailPesanan());
            return repository.save(pesanan);
        });
    }

    public boolean delete(Long id) {
        if (repository.existsById(id)) {
            repository.deleteById(id);
            return true;
        }
        return false;
    }
}
