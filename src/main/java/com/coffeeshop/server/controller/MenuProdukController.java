package com.coffeeshop.server.controller;

import com.coffeeshop.server.dto.ApiResponse;
import com.coffeeshop.server.model.MenuProduk;
import com.coffeeshop.server.service.MenuProdukService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/menu-produk")
public class MenuProdukController {

    @Autowired
    private MenuProdukService service;

    @GetMapping
    public ResponseEntity<ApiResponse> getAllMenu() {
        List<MenuProduk> data = service.findAll();
        return ResponseEntity.ok(new ApiResponse(true, "Success", data));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse> getMenuById(@PathVariable Long id) {
        return service.findById(id)
                .map(menu -> ResponseEntity.ok(new ApiResponse(true, "Success", menu)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Menu not found", null)));
    }

    @PostMapping
    public ResponseEntity<ApiResponse> createMenu(@RequestBody MenuProduk menu) {
        MenuProduk saved = service.save(menu);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new ApiResponse(true, "Produk berhasil ditambahkan", saved));
    }

    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse> updateMenu(@PathVariable Long id, @RequestBody MenuProduk menuDetails) {
        return service.update(id, menuDetails)
                .map(menu -> ResponseEntity.ok(new ApiResponse(true, "Produk berhasil diupdate", menu)))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Menu not found", null)));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse> deleteMenu(@PathVariable Long id) {
        if (service.delete(id)) {
            return ResponseEntity.ok(new ApiResponse(true, "Produk berhasil dihapus", null));
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ApiResponse(false, "Menu not found", null));
    }
}
