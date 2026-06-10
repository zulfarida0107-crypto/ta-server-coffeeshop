package com.coffeeshop.server.controller;

import com.coffeeshop.server.dto.ApiResponse;
import com.coffeeshop.server.dto.LoginRequest;
import com.coffeeshop.server.dto.LoginResponse;
import com.coffeeshop.server.model.User;
import com.coffeeshop.server.repository.UserRepository;
import com.coffeeshop.server.security.JwtTokenProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtTokenProvider tokenProvider;

    @PostMapping("/login")
    public ResponseEntity<ApiResponse> login(@RequestBody LoginRequest loginRequest) {
        String username = loginRequest.getUsername();
        String password = loginRequest.getPassword();

        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            // Matching password (plain text as per current system design for this TA)
            if (user.getPassword().equals(password)) {
                String token = tokenProvider.generateToken(username);
                LoginResponse loginResponse = new LoginResponse(token, user);
                return ResponseEntity.ok(new ApiResponse(true, "Login successful", loginResponse));
            }
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(new ApiResponse(false, "Invalid credentials", null));
    }
}
