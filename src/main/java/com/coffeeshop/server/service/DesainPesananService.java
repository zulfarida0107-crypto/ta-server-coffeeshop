package com.coffeeshop.server.service;

import com.coffeeshop.server.model.DesainPesanan;
import com.coffeeshop.server.repository.DesainPesananRepository;
import com.coffeeshop.server.repository.PesananRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class DesainPesananService {

    @Autowired
    private DesainPesananRepository repository;

    @Autowired
    private PesananRepository pesananRepository;

    public List<DesainPesanan> findAll() {
        return repository.findAll();
    }

    public Optional<DesainPesanan> findById(Long id) {
        return repository.findById(id);
    }

    public DesainPesanan save(DesainPesanan desainPesanan) {
        DesainPesanan saved = repository.save(desainPesanan);
        syncStatusToPesanan(saved.getIdPesanan(), saved.getStatusPesanan());
        return saved;
    }

    public Optional<DesainPesanan> update(Long id, DesainPesanan desainDetails) {
        return repository.findById(id).map(desain -> {
            desain.setIdPesanan(desainDetails.getIdPesanan());
            desain.setFileDesainUrl(desainDetails.getFileDesainUrl());
            desain.setKeterangan(desainDetails.getKeterangan());
            desain.setTanggalUpload(desainDetails.getTanggalUpload());
            desain.setStatusPesanan(desainDetails.getStatusPesanan());
            
            DesainPesanan updated = repository.save(desain);
            syncStatusToPesanan(updated.getIdPesanan(), updated.getStatusPesanan());
            return updated;
        });
    }

    private void syncStatusToPesanan(Long idPesanan, String status) {
        if (idPesanan != null && status != null) {
            if ("Proses".equalsIgnoreCase(status) || "Selesai".equalsIgnoreCase(status)) {
                pesananRepository.findById(idPesanan).ifPresent(pesanan -> {
                    pesanan.setStatusPesanan(status);
                    pesananRepository.save(pesanan);
                });
            }
        }
    }

    public boolean delete(Long id) {
        if (repository.existsById(id)) {
            repository.deleteById(id);
            return true;
        }
        return false;
    }
}
