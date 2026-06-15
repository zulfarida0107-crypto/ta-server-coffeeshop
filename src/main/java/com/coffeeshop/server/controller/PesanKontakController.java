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

    @Autowired
    private org.springframework.mail.javamail.JavaMailSender mailSender;

    @org.springframework.beans.factory.annotation.Value("${spring.mail.password:}")
    private String mailPassword;

    @PostMapping("/{id}/balas")
    public ResponseEntity<ApiResponse> kirimBalasan(@PathVariable Long id, @RequestBody java.util.Map<String, String> request) {
        String isiBalasan = request.get("pesan");
        if (isiBalasan == null || isiBalasan.trim().isEmpty()) {
            return ResponseEntity.badRequest().body(new ApiResponse(false, "Balasan tidak boleh kosong", null));
        }

        return service.findById(id)
                .map(pesan -> {
                    try {
                        if (mailPassword == null || mailPassword.contains("placeholder") || mailPassword.trim().isEmpty()) {
                            System.out.println("==================================================");
                            System.out.println("[SIMULASI EMAIL] Mengirim email terprogram...");
                            System.out.println("Dari: zulfarida0107@gmail.com");
                            System.out.println("Kepada: " + pesan.getEmail());
                            System.out.println("Subjek: Balasan: " + pesan.getSubjek());
                            System.out.println("Isi Pesan: " + isiBalasan);
                            System.out.println("==================================================");
                            pesan.setSudahDibalas(true);
                            service.save(pesan);
                            return ResponseEntity.ok(new ApiResponse(true, "Simulasi balasan berhasil terkirim langsung!", null));
                        }

                        org.springframework.mail.SimpleMailMessage message = new org.springframework.mail.SimpleMailMessage();
                        message.setFrom("zulfarida0107@gmail.com");
                        message.setTo(pesan.getEmail());
                        message.setSubject("Balasan: " + pesan.getSubjek());
                        message.setText(isiBalasan);
                        
                        mailSender.send(message);
                        pesan.setSudahDibalas(true);
                        service.save(pesan);
                        return ResponseEntity.ok(new ApiResponse(true, "Balasan berhasil dikirim ke " + pesan.getEmail(), null));
                    } catch (Exception e) {
                        e.printStackTrace();
                        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                .body(new ApiResponse(false, "Gagal mengirim email: " + e.getMessage(), null));
                    }
                })
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(new ApiResponse(false, "Pesan not found", null)));
    }

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
