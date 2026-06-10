package com.coffeeshop.server.service;

import com.coffeeshop.server.model.PesanKontak;
import com.coffeeshop.server.repository.PesanKontakRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PesanKontakService {

    @Autowired
    private PesanKontakRepository repository;

    public List<PesanKontak> findAll() {
        return repository.findAll();
    }

    public Optional<PesanKontak> findById(Long id) {
        return repository.findById(id);
    }

    public PesanKontak save(PesanKontak pesan) {
        return repository.save(pesan);
    }

    public boolean delete(Long id) {
        if (repository.existsById(id)) {
            repository.deleteById(id);
            return true;
        }
        return false;
    }

    public void deleteAll() {
        repository.deleteAll();
    }
}
