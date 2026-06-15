package com.coffeeshop.server.config;

import com.coffeeshop.server.security.JwtAuthFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private JwtAuthFilter jwtAuthFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .cors(cors -> cors.configure(http))
                .csrf(AbstractHttpConfigurer::disable)
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/auth/**").permitAll() // Jalur login/register

                        // --- BUKA SEMUA AKSES CRUD (GET, POST, PUT, DELETE) SEMENTARA ---

                        // 1. menu_produk
                        .requestMatchers("/api/menu-produk", "/api/menu-produk/**").permitAll()

                        // 2. desain_pesanan
                        .requestMatchers("/api/desain-pesanan", "/api/desain-pesanan/**").permitAll()

                        // 3. pesanan
                        .requestMatchers("/api/pesanan", "/api/pesanan/**").permitAll()

                        // 4. pesan_kontak
                        .requestMatchers("/api/pesan-kontak", "/api/pesan-kontak/**").permitAll()

                        // 5. user
                        .requestMatchers("/api/user", "/api/user/**").permitAll()

                        // 6. Buka jalur error agar Postman menampilkan 404 Not Found (bukan 403
                        // Forbidden)
                        .requestMatchers("/", "/error").permitAll()

                        // Endpoint lain di luar 5 tabel di atas akan tetap diblokir
                        .anyRequest().authenticated());

        http.addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}