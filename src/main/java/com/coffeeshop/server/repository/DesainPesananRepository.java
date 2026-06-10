package com.coffeeshop.server.repository;

import com.coffeeshop.server.model.DesainPesanan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DesainPesananRepository extends JpaRepository<DesainPesanan, Long> {
}
