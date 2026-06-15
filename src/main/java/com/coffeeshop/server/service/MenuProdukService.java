package com.coffeeshop.server.service;

import com.coffeeshop.server.model.MenuProduk;
import com.coffeeshop.server.repository.MenuProdukRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class MenuProdukService {

    @Autowired
    private MenuProdukRepository repository;

    public List<MenuProduk> findAll() {
        return repository.findAll();
    }

    public Optional<MenuProduk> findById(Long id) {
        return repository.findById(id);
    }

    public MenuProduk save(MenuProduk menu) {
        return repository.save(menu);
    }

    public Optional<MenuProduk> update(Long id, MenuProduk menuDetails) {
        return repository.findById(id).map(menu -> {
            menu.setNamaProduk(menuDetails.getNamaProduk());
            menu.setHarga(menuDetails.getHarga());
            menu.setDeskripsi(menuDetails.getDeskripsi());
            menu.setKategori(menuDetails.getKategori());
            menu.setGambar(menuDetails.getGambar());
            return repository.save(menu);
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
