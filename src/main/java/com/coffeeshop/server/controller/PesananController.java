package com.coffeeshop.server.controller;

import com.coffeeshop.server.dto.ApiResponse;
import com.coffeeshop.server.model.Pesanan;
import com.coffeeshop.server.service.PesananService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/pesanan")
public class PesananController {

    @Autowired
    private PesananService service;

    @GetMapping
    public ResponseEntity<ApiResponse> getAllPesanan() {
        List<Pesanan> data = service.findAll();
        return ResponseEntity.ok(new ApiResponse(true, "Success", data));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse> getPesananById(@PathVariable Long id) {
        return service.findById(id)
                .map(pesanan -> ResponseEntity.ok(new ApiResponse(true, "Success", pesanan)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Pesanan not found", null)));
    }

    @PostMapping
    public ResponseEntity<ApiResponse> createPesanan(@RequestBody Pesanan pesanan) {
        Pesanan saved = service.save(pesanan);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new ApiResponse(true, "Pesanan berhasil ditambahkan", saved));
    }

    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse> updatePesanan(@PathVariable Long id, @RequestBody Pesanan pesananDetails) {
        return service.update(id, pesananDetails)
                .map(pesanan -> ResponseEntity.ok(new ApiResponse(true, "Pesanan berhasil diupdate", pesanan)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Pesanan not found", null)));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse> deletePesanan(@PathVariable Long id) {
        if (service.delete(id)) {
            return ResponseEntity.ok(new ApiResponse(true, "Pesanan berhasil dihapus", null));
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ApiResponse(false, "Pesanan not found", null));
    }
}
