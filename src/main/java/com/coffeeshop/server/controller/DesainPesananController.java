package com.coffeeshop.server.controller;

import com.coffeeshop.server.dto.ApiResponse;
import com.coffeeshop.server.model.DesainPesanan;
import com.coffeeshop.server.service.DesainPesananService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/desain-pesanan")
public class DesainPesananController {

    @Autowired
    private DesainPesananService service;

    @GetMapping
    public ResponseEntity<ApiResponse> getAllDesainPesanan() {
        List<DesainPesanan> data = service.findAll();
        return ResponseEntity.ok(new ApiResponse(true, "Success", data));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse> getDesainPesananById(@PathVariable Long id) {
        return service.findById(id)
                .map(desain -> ResponseEntity.ok(new ApiResponse(true, "Success", desain)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Desain not found", null)));
    }

    @PostMapping
    public ResponseEntity<ApiResponse> createDesainPesanan(@RequestBody DesainPesanan desainPesanan) {
        DesainPesanan saved = service.save(desainPesanan);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new ApiResponse(true, "Desain berhasil ditambahkan", saved));
    }

    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse> updateDesainPesanan(@PathVariable Long id, @RequestBody DesainPesanan desainDetails) {
        return service.update(id, desainDetails)
                .map(desain -> ResponseEntity.ok(new ApiResponse(true, "Desain berhasil diupdate", desain)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Desain not found", null)));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse> deleteDesainPesanan(@PathVariable Long id) {
        if (service.delete(id)) {
            return ResponseEntity.ok(new ApiResponse(true, "Desain berhasil dihapus", null));
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ApiResponse(false, "Desain not found", null));
    }
}
