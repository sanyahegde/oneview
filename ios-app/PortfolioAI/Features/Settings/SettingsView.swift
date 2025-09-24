//  SettingsView.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var container: DIContainer
    @State private var showingLogoutAlert = false
    
    var body: some View {
        NavigationView {
            List {
                // User Section
                Section {
                    UserProfileRow(user: authManager.currentUser)
                } header: {
                    Text("Profile")
                }
                
                // App Settings Section
                Section {
                    SettingsRow(
                        icon: "bell.fill",
                        title: "Notifications",
                        subtitle: "Manage your alerts"
                    ) {
                        // Handle notifications settings
                    }
                    
                    SettingsRow(
                        icon: "lock.fill",
                        title: "Privacy & Security",
                        subtitle: "Manage your data and security"
                    ) {
                        // Handle privacy settings
                    }
                    
                    SettingsRow(
                        icon: "chart.bar.fill",
                        title: "Portfolio Settings",
                        subtitle: "Customize your portfolio view"
                    ) {
                        // Handle portfolio settings
                    }
                } header: {
                    Text("Settings")
                }
                
                // Support Section
                Section {
                    SettingsRow(
                        icon: "questionmark.circle.fill",
                        title: "Help & Support",
                        subtitle: "Get help and contact support"
                    ) {
                        // Handle help
                    }
                    
                    SettingsRow(
                        icon: "doc.text.fill",
                        title: "Terms & Privacy",
                        subtitle: "Read our terms and privacy policy"
                    ) {
                        // Handle terms
                    }
                    
                    SettingsRow(
                        icon: "info.circle.fill",
                        title: "About",
                        subtitle: "App version and information"
                    ) {
                        // Handle about
                    }
                } header: {
                    Text("Support")
                }
                
                // Logout Section
                Section {
                    Button(action: { showingLogoutAlert = true }) {
                        HStack {
                            Image(systemName: "rectangle.portrait.and.arrow.right")
                                .foregroundColor(.errorRed)
                                .frame(width: 24)
                            
                            Text("Sign Out")
                                .foregroundColor(.errorRed)
                            
                            Spacer()
                        }
                    }
                }
            }
            .navigationTitle("Settings")
            .alert("Sign Out", isPresented: $showingLogoutAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Sign Out", role: .destructive) {
                    authManager.logout()
                }
            } message: {
                Text("Are you sure you want to sign out?")
            }
        }
    }
}

struct UserProfileRow: View {
    let user: User?
    
    var body: some View {
        HStack {
            // Profile Avatar
            Circle()
                .fill(Color.primaryBlue)
                .frame(width: 50, height: 50)
                .overlay(
                    Text(user?.fullName?.prefix(1).uppercased() ?? "U")
                        .font(.title2)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                )
            
            VStack(alignment: .leading, spacing: 4) {
                Text(user?.fullName ?? "User")
                    .font(.headline)
                
                Text(user?.email ?? "user@example.com")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
        }
        .padding(.vertical, 8)
    }
}

struct SettingsRow: View {
    let icon: String
    let title: String
    let subtitle: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(.primaryBlue)
                    .frame(width: 24)
                
                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(.body)
                        .foregroundColor(.primary)
                    
                    Text(subtitle)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding(.vertical, 4)
        }
        .buttonStyle(PlainButtonStyle())
    }
}
