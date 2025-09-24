//  PortfolioAIApp.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import SwiftUI
import LocalAuthentication

@main
struct PortfolioAIApp: App {
    @StateObject private var authManager = AuthenticationManager()
    @StateObject private var container = DIContainer()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authManager)
                .environmentObject(container)
                .onAppear {
                    setupAppearance()
                }
        }
    }
    
    private func setupAppearance() {
        // Configure app appearance
        UINavigationBar.appearance().largeTitleTextAttributes = [
            .foregroundColor: UIColor(Color.primary)
        ]
        UINavigationBar.appearance().titleTextAttributes = [
            .foregroundColor: UIColor(Color.primary)
        ]
    }
}

struct ContentView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var container: DIContainer
    
    var body: some View {
        Group {
            if authManager.isAuthenticated {
                MainTabView()
            } else {
                LoginView()
            }
        }
        .onAppear {
            authManager.checkAuthenticationStatus()
        }
    }
}

struct MainTabView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    
    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Image(systemName: "chart.line.uptrend.xyaxis")
                    Text("Overview")
                }
            
            HoldingsView()
                .tabItem {
                    Image(systemName: "briefcase.fill")
                    Text("Holdings")
                }
            
            AccountsLinkView()
                .tabItem {
                    Image(systemName: "link")
                    Text("Accounts")
                }
            
            SettingsView()
                .tabItem {
                    Image(systemName: "gear")
                    Text("Settings")
                }
        }
        .accentColor(.blue)
    }
}
