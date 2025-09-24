//  LoginView.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import SwiftUI
import LocalAuthentication

struct LoginView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @State private var email = ""
    @State private var password = ""
    @State private var fullName = ""
    @State private var isRegistering = false
    @State private var isLoading = false
    @State private var errorMessage = ""
    @State private var showBiometricAuth = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.sectionSpacing) {
                // Header
                VStack(spacing: Theme.itemSpacing) {
                    Image(systemName: "chart.line.uptrend.xyaxis")
                        .font(.system(size: 60))
                        .foregroundColor(.primaryBlue)
                    
                    Text("PortfolioAI")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Text("Your unified portfolio manager")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                .padding(.top, 40)
                
                Spacer()
                
                // Form
                VStack(spacing: Theme.itemSpacing) {
                    if isRegistering {
                        TextField("Full Name", text: $fullName)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .autocapitalization(.words)
                    }
                    
                    TextField("Email", text: $email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                    
                    SecureField("Password", text: $password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                
                // Error Message
                if !errorMessage.isEmpty {
                    Text(errorMessage)
                        .foregroundColor(.errorRed)
                        .font(.caption)
                }
                
                // Action Buttons
                VStack(spacing: Theme.itemSpacing) {
                    Button(action: handlePrimaryAction) {
                        HStack {
                            if isLoading {
                                ProgressView()
                                    .scaleEffect(0.8)
                            }
                            Text(isRegistering ? "Sign Up" : "Sign In")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.primaryBlue)
                        .foregroundColor(.white)
                        .cornerRadius(Theme.cornerRadius)
                    }
                    .disabled(isLoading || email.isEmpty || password.isEmpty)
                    
                    Button(action: toggleAuthMode) {
                        Text(isRegistering ? "Already have an account? Sign In" : "Don't have an account? Sign Up")
                            .font(.caption)
                            .foregroundColor(.primaryBlue)
                    }
                }
                
                // Biometric Authentication
                if !isRegistering && !showBiometricAuth {
                    Button(action: authenticateWithBiometrics) {
                        HStack {
                            Image(systemName: "faceid")
                            Text("Use Face ID")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.secondaryBackground)
                        .foregroundColor(.primary)
                        .cornerRadius(Theme.cornerRadius)
                    }
                }
                
                Spacer()
            }
            .padding(.horizontal, Theme.cardPadding)
            .navigationBarHidden(true)
        }
    }
    
    private func handlePrimaryAction() {
        isLoading = true
        errorMessage = ""
        
        if isRegistering {
            authManager.register(email: email, password: password, fullName: fullName) { result in
                handleAuthResult(result)
            }
        } else {
            authManager.login(email: email, password: password) { result in
                handleAuthResult(result)
            }
        }
    }
    
    private func handleAuthResult(_ result: Result<Void, Error>) {
        isLoading = false
        
        switch result {
        case .success:
            break // Navigation handled by authManager
        case .failure(let error):
            errorMessage = error.localizedDescription
        }
    }
    
    private func toggleAuthMode() {
        isRegistering.toggle()
        errorMessage = ""
    }
    
    private func authenticateWithBiometrics() {
        let context = LAContext()
        var error: NSError?
        
        if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
            context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: "Authenticate to access your portfolio") { success, error in
                DispatchQueue.main.async {
                    if success {
                        // Try to login with stored credentials
                        // For demo purposes, use demo credentials
                        authManager.login(email: "demo@portfolioai.com", password: "demo123") { _ in
                            // Handle result
                        }
                    }
                }
            }
        }
    }
}
