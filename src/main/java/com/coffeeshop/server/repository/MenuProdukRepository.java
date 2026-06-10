package com.coffeeshop.server.repository;

import com.coffeeshop.server.model.MenuProduk;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MenuProdukRepository extends JpaRepository<MenuProduk, Long> {
}
