//  HoldingsView.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import SwiftUI

struct HoldingsView: View {
    @EnvironmentObject var container: DIContainer
    @State private var holdings: [UnifiedHolding] = []
    @State private var isLoading = true
    @State private var searchText = ""
    @State private var sortOption: SortOption = .value
    
    enum SortOption: String, CaseIterable {
        case symbol = "Symbol"
        case value = "Value"
        case change = "Change"
        case quantity = "Quantity"
    }
    
    var filteredAndSortedHoldings: [UnifiedHolding] {
        var filtered = holdings
        
        // Filter by search text
        if !searchText.isEmpty {
            filtered = filtered.filter { holding in
                holding.symbol.localizedCaseInsensitiveContains(searchText)
            }
        }
        
        // Sort holdings
        switch sortOption {
        case .symbol:
            filtered.sort { $0.symbol < $1.symbol }
        case .value:
            filtered.sort { $0.value > $1.value }
        case .change:
            filtered.sort { $0.gainLoss > $1.gainLoss }
        case .quantity:
            filtered.sort { $0.quantity > $1.quantity }
        }
        
        return filtered
    }
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Search and Sort Controls
                VStack(spacing: Theme.itemSpacing) {
                    SearchBar(text: $searchText)
                    
                    HStack {
                        Text("Sort by:")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Picker("Sort", selection: $sortOption) {
                            ForEach(SortOption.allCases, id: \.self) { option in
                                Text(option.rawValue).tag(option)
                            }
                        }
                        .pickerStyle(SegmentedPickerStyle())
                    }
                }
                .padding(.horizontal, Theme.cardPadding)
                .padding(.vertical, Theme.itemSpacing)
                .background(Color.secondaryBackground)
                
                // Holdings List
                if isLoading {
                    ProgressView("Loading holdings...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if filteredAndSortedHoldings.isEmpty {
                    EmptyHoldingsView()
                } else {
                    List(filteredAndSortedHoldings, id: \.symbol) { holding in
                        HoldingDetailRowView(holding: holding)
                            .listRowInsets(EdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16))
                    }
                    .listStyle(PlainListStyle())
                }
            }
            .navigationTitle("Holdings")
            .refreshable {
                loadHoldings()
            }
        }
        .onAppear {
            loadHoldings()
        }
    }
    
    private func loadHoldings() {
        isLoading = true
        
        container.apiClient.getHoldings { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let holdings):
                    self.holdings = holdings
                case .failure(let error):
                    print("Error loading holdings: \(error)")
                }
                self.isLoading = false
            }
        }
    }
}

struct SearchBar: View {
    @Binding var text: String
    
    var body: some View {
        HStack {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.secondary)
            
            TextField("Search holdings...", text: $text)
                .textFieldStyle(PlainTextFieldStyle())
            
            if !text.isEmpty {
                Button(action: { text = "" }) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(Color(.systemGray6))
        .cornerRadius(8)
    }
}

struct HoldingDetailRowView: View {
    let holding: UnifiedHolding
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.itemSpacing) {
            // Header
            HStack {
                VStack(alignment: .leading) {
                    Text(holding.symbol)
                        .font(.headline)
                        .fontWeight(.semibold)
                    
                    Text(holding.accountName ?? "Unknown Account")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                VStack(alignment: .trailing) {
                    Text("$\(holding.value, specifier: "%.2f")")
                        .font(.headline)
                        .fontWeight(.semibold)
                    
                    Text("\(holding.quantity, specifier: "%.2f") shares")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            // Details
            HStack {
                VStack(alignment: .leading) {
                    Text("Avg Cost")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text("$\(holding.avgCost, specifier: "%.2f")")
                        .font(.subheadline)
                }
                
                Spacer()
                
                VStack(alignment: .center) {
                    Text("Current Price")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text("$\(holding.currentPrice, specifier: "%.2f")")
                        .font(.subheadline)
                }
                
                Spacer()
                
                VStack(alignment: .trailing) {
                    Text("Gain/Loss")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    let gainLoss = holding.value - (holding.quantity * holding.avgCost)
                    let gainLossPercent = (gainLoss / (holding.quantity * holding.avgCost)) * 100
                    
                    VStack(alignment: .trailing) {
                        Text("$\(gainLoss, specifier: "%.2f")")
                            .font(.subheadline)
                            .foregroundColor(gainLoss >= 0 ? .positiveChange : .negativeChange)
                        
                        Text("(\(gainLossPercent, specifier: "%.2f")%)")
                            .font(.caption)
                            .foregroundColor(gainLoss >= 0 ? .positiveChange : .negativeChange)
                    }
                }
            }
        }
        .padding(Theme.cardPadding)
        .background(Color.cardBackground)
        .cornerRadius(Theme.cornerRadius)
        .shadow(radius: 1)
    }
}

struct EmptyHoldingsView: View {
    var body: some View {
        VStack(spacing: Theme.sectionSpacing) {
            Image(systemName: "briefcase")
                .font(.system(size: 60))
                .foregroundColor(.secondary)
            
            Text("No Holdings")
                .font(.title2)
                .fontWeight(.semibold)
            
            Text("Link your accounts to see your holdings here")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            
            NavigationLink(destination: AccountsLinkView()) {
                Text("Link Account")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.primaryBlue)
                    .cornerRadius(Theme.cornerRadius)
            }
        }
        .padding(Theme.cardPadding)
    }
}
