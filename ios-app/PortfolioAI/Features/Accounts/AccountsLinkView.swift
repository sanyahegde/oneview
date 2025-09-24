//  AccountsLinkView.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import SwiftUI

struct AccountsLinkView: View {
    @EnvironmentObject var container: DIContainer
    @State private var accounts: [Account] = []
    @State private var isLoading = true
    @State private var isLinking = false
    @State private var selectedProvider: Provider = .robinhood
    @State private var showLinkSheet = false
    @State private var errorMessage = ""
    
    enum Provider: String, CaseIterable {
        case robinhood = "robinhood"
        case schwab = "schwab"
        case plaid = "plaid"
        case akoya = "akoya"
        
        var displayName: String {
            switch self {
            case .robinhood: return "Robinhood"
            case .schwab: return "Charles Schwab"
            case .plaid: return "Plaid (Banks)"
            case .akoya: return "Akoya (Banks)"
            }
        }
        
        var icon: String {
            switch self {
            case .robinhood: return "chart.line.uptrend.xyaxis"
            case .schwab: return "building.2"
            case .plaid: return "banknote"
            case .akoya: return "creditcard"
            }
        }
        
        var description: String {
            switch self {
            case .robinhood: return "Connect your Robinhood brokerage account"
            case .schwab: return "Connect your Charles Schwab account"
            case .plaid: return "Connect your bank accounts via Plaid"
            case .akoya: return "Connect your bank accounts via Akoya"
            }
        }
    }
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.sectionSpacing) {
                if isLoading {
                    ProgressView("Loading accounts...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    // Linked Accounts Section
                    if !accounts.isEmpty {
                        LinkedAccountsSection(accounts: accounts)
                    }
                    
                    // Link New Account Section
                    LinkNewAccountSection(
                        selectedProvider: $selectedProvider,
                        showLinkSheet: $showLinkSheet
                    )
                }
                
                // Error Message
                if !errorMessage.isEmpty {
                    Text(errorMessage)
                        .foregroundColor(.errorRed)
                        .font(.caption)
                        .padding(.horizontal, Theme.cardPadding)
                }
            }
            .navigationTitle("Accounts")
            .refreshable {
                loadAccounts()
            }
            .sheet(isPresented: $showLinkSheet) {
                LinkAccountSheet(
                    provider: selectedProvider,
                    isLinking: $isLinking,
                    onSuccess: {
                        showLinkSheet = false
                        loadAccounts()
                    },
                    onError: { error in
                        errorMessage = error.localizedDescription
                    }
                )
            }
        }
        .onAppear {
            loadAccounts()
        }
    }
    
    private func loadAccounts() {
        isLoading = true
        errorMessage = ""
        
        container.apiClient.getAccounts { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let accounts):
                    self.accounts = accounts
                case .failure(let error):
                    self.errorMessage = error.localizedDescription
                }
                self.isLoading = false
            }
        }
    }
}

struct LinkedAccountsSection: View {
    let accounts: [Account]
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.itemSpacing) {
            Text("Linked Accounts")
                .font(.headline)
                .padding(.horizontal, Theme.cardPadding)
            
            ForEach(accounts, id: \.id) { account in
                AccountCard(account: account)
            }
        }
    }
}

struct LinkNewAccountSection: View {
    @Binding var selectedProvider: AccountsLinkView.Provider
    @Binding var showLinkSheet: Bool
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.itemSpacing) {
            Text("Link New Account")
                .font(.headline)
                .padding(.horizontal, Theme.cardPadding)
            
            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: Theme.itemSpacing) {
                ForEach(AccountsLinkView.Provider.allCases, id: \.self) { provider in
                    ProviderCard(
                        provider: provider,
                        onTap: {
                            selectedProvider = provider
                            showLinkSheet = true
                        }
                    )
                }
            }
            .padding(.horizontal, Theme.cardPadding)
        }
    }
}

struct AccountCard: View {
    let account: Account
    
    var body: some View {
        HStack {
            Image(systemName: providerIcon(account.provider))
                .font(.title2)
                .foregroundColor(.primaryBlue)
                .frame(width: 40)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(account.name ?? "Unknown Account")
                    .font(.headline)
                
                Text(providerDisplayName(account.provider))
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                if let lastSync = account.lastSync {
                    Text("Last synced: \(lastSync, formatter: dateFormatter)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
            
            VStack {
                Text(account.accountType.capitalized)
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.secondaryBackground)
                    .cornerRadius(8)
                
                Image(systemName: "checkmark.circle.fill")
                    .foregroundColor(.successGreen)
            }
        }
        .padding(Theme.cardPadding)
        .background(Color.cardBackground)
        .cornerRadius(Theme.cornerRadius)
        .shadow(radius: 1)
        .padding(.horizontal, Theme.cardPadding)
    }
    
    private func providerIcon(_ provider: String) -> String {
        switch provider {
        case "robinhood": return "chart.line.uptrend.xyaxis"
        case "schwab": return "building.2"
        case "plaid": return "banknote"
        case "akoya": return "creditcard"
        default: return "questionmark.circle"
        }
    }
    
    private func providerDisplayName(_ provider: String) -> String {
        switch provider {
        case "robinhood": return "Robinhood"
        case "schwab": return "Charles Schwab"
        case "plaid": return "Plaid"
        case "akoya": return "Akoya"
        default: return provider.capitalized
        }
    }
    
    private let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter
    }()
}

struct ProviderCard: View {
    let provider: AccountsLinkView.Provider
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            VStack(spacing: Theme.itemSpacing) {
                Image(systemName: provider.icon)
                    .font(.system(size: 30))
                    .foregroundColor(.primaryBlue)
                
                Text(provider.displayName)
                    .font(.headline)
                    .multilineTextAlignment(.center)
                
                Text(provider.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
            }
            .padding(Theme.cardPadding)
            .frame(maxWidth: .infinity)
            .background(Color.cardBackground)
            .cornerRadius(Theme.cornerRadius)
            .shadow(radius: 1)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct LinkAccountSheet: View {
    let provider: AccountsLinkView.Provider
    @Binding var isLinking: Bool
    let onSuccess: () -> Void
    let onError: (Error) -> Void
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.sectionSpacing) {
                // Header
                VStack(spacing: Theme.itemSpacing) {
                    Image(systemName: provider.icon)
                        .font(.system(size: 60))
                        .foregroundColor(.primaryBlue)
                    
                    Text("Link \(provider.displayName)")
                        .font(.title)
                        .fontWeight(.bold)
                    
                    Text(provider.description)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
                .padding(.top, 40)
                
                Spacer()
                
                // Mock Link Process
                VStack(spacing: Theme.itemSpacing) {
                    Text("This is a demo app. In production, this would:")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("• Open \(provider.displayName) authentication")
                        Text("• Exchange public token for access token")
                        Text("• Sync account data securely")
                        Text("• Store encrypted credentials")
                    }
                    .font(.caption)
                    .foregroundColor(.secondary)
                }
                
                Spacer()
                
                // Action Buttons
                VStack(spacing: Theme.itemSpacing) {
                    Button(action: linkAccount) {
                        HStack {
                            if isLinking {
                                ProgressView()
                                    .scaleEffect(0.8)
                            }
                            Text("Link Account (Demo)")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.primaryBlue)
                        .foregroundColor(.white)
                        .cornerRadius(Theme.cornerRadius)
                    }
                    .disabled(isLinking)
                    
                    Button("Cancel") {
                        dismiss()
                    }
                    .foregroundColor(.secondary)
                }
            }
            .padding(.horizontal, Theme.cardPadding)
            .navigationBarTitleDisplayMode(.inline)
            .navigationBarBackButtonHidden(true)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
    }
    
    private func linkAccount() {
        isLinking = true
        
        // Simulate linking process
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            isLinking = false
            onSuccess()
        }
    }
}
