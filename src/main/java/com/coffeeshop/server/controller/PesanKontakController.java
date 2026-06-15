package com.coffeeshop.server.controller;

import com.coffeeshop.server.dto.ApiResponse;
import com.coffeeshop.server.model.PesanKontak;
import com.coffeeshop.server.service.PesanKontakService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/pesan-kontak")
public class PesanKontakController {

    @Autowired
    private PesanKontakService service;

    @GetMapping
    public ResponseEntity<ApiResponse> getAllPesanKontak() {
        List<PesanKontak> data = service.findAll();
        return ResponseEntity.ok(new ApiResponse(true, "Success", data));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse> getPesanKontakById(@PathVariable Long id) {
        return service.findById(id)
                .map(pesan -> ResponseEntity.ok(new ApiResponse(true, "Success", pesan)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Pesan not found", null)));
    }

    @PostMapping
    public ResponseEntity<ApiResponse> createPesanKontak(@RequestBody PesanKontak pesan) {
        PesanKontak saved = service.save(pesan);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new ApiResponse(true, "Pesan berhasil ditambahkan", saved));
    }

    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse> updatePesanKontak(@PathVariable Long id, @RequestBody PesanKontak pesanDetails) {
        return service.findById(id)
                .map(pesan -> {
                    // Update nilai-nilainya dengan data baru dari Postman
                    pesan.setNama(pesanDetails.getNama());
                    pesan.setEmail(pesanDetails.getEmail());
                    pesan.setSubjek(pesanDetails.getSubjek());
                    pesan.setPesan(pesanDetails.getPesan());

                    // Simpan kembali ke database
                    PesanKontak updatedPesan = service.save(pesan);
                    return ResponseEntity.ok(new ApiResponse(true, "Pesan berhasil diupdate", updatedPesan));
                })
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Pesan not found", null)));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse> deletePesanKontak(@PathVariable Long id) {
        if (service.delete(id)) {
            return ResponseEntity.ok(new ApiResponse(true, "Pesan berhasil dihapus", null));
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ApiResponse(false, "Pesan not found", null));
    }

    @DeleteMapping("/all")
    public ResponseEntity<ApiResponse> deleteAllPesanKontak() {
        service.deleteAll();
        return ResponseEntity.ok(new ApiResponse(true, "Semua pesan berhasil dihapus", null));
    }
}
