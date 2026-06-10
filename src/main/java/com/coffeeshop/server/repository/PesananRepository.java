package com.coffeeshop.server.repository;

import com.coffeeshop.server.model.Pesanan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PesananRepository extends JpaRepository<Pesanan, Long> {
}
