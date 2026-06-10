package com.coffeeshop.server.repository;

import com.coffeeshop.server.model.PesanKontak;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PesanKontakRepository extends JpaRepository<PesanKontak, Long> {
}
