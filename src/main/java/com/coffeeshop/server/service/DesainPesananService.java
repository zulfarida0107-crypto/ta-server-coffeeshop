package com.coffeeshop.server.service;

import com.coffeeshop.server.model.DesainPesanan;
import com.coffeeshop.server.repository.DesainPesananRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class DesainPesananService {

    @Autowired
    private DesainPesananRepository repository;

    public List<DesainPesanan> findAll() {
        return repository.findAll();
    }

    public Optional<DesainPesanan> findById(Long id) {
        return repository.findById(id);
    }

    public DesainPesanan save(DesainPesanan desainPesanan) {
        return repository.save(desainPesanan);
    }

    public Optional<DesainPesanan> update(Long id, DesainPesanan desainDetails) {
        return repository.findById(id).map(desain -> {
            desain.setIdPesanan(desainDetails.getIdPesanan());
            desain.setFileDesainUrl(desainDetails.getFileDesainUrl());
            desain.setKeterangan(desainDetails.getKeterangan());
            desain.setTanggalUpload(desainDetails.getTanggalUpload());
            return repository.save(desain);
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
