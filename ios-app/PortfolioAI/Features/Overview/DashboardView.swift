//  DashboardView.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import SwiftUI
import Charts

struct DashboardView: View {
    @EnvironmentObject var container: DIContainer
    @State private var portfolioData: PortfolioData?
    @State private var holdings: [UnifiedHolding] = []
    @State private var isLoading = true
    @State private var errorMessage = ""
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.sectionSpacing) {
                    if isLoading {
                        ProgressView("Loading portfolio...")
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                    } else if let data = portfolioData {
                        // Portfolio Summary Card
                        PortfolioSummaryCard(data: data)
                        
                        // Performance Chart
                        PerformanceChartCard(data: data)
                        
                        // Top Holdings
                        TopHoldingsCard(holdings: holdings)
                        
                        // News Sentiment
                        NewsSentimentCard()
                    } else {
                        ErrorView(message: errorMessage) {
                            loadData()
                        }
                    }
                }
                .padding(.horizontal, Theme.cardPadding)
            }
            .navigationTitle("Portfolio")
            .refreshable {
                loadData()
            }
        }
        .onAppear {
            loadData()
        }
    }
    
    private func loadData() {
        isLoading = true
        errorMessage = ""
        
        // Load portfolio data
        container.apiClient.getPortfolioSummary { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let data):
                    self.portfolioData = data
                case .failure(let error):
                    self.errorMessage = error.localizedDescription
                }
            }
        }
        
        // Load holdings
        container.apiClient.getHoldings { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let holdings):
                    self.holdings = holdings
                case .failure(let error):
                    self.errorMessage = error.localizedDescription
                }
                self.isLoading = false
            }
        }
    }
}

struct PortfolioSummaryCard: View {
    let data: PortfolioData
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.itemSpacing) {
            Text("Total Portfolio Value")
                .font(.headline)
                .foregroundColor(.secondary)
            
            Text("$\(data.totalValue, specifier: "%.2f")")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            HStack {
                Image(systemName: data.gainLoss >= 0 ? "arrow.up.right" : "arrow.down.right")
                    .foregroundColor(data.gainLoss >= 0 ? .positiveChange : .negativeChange)
                
                Text("$\(abs(data.gainLoss), specifier: "%.2f")")
                    .foregroundColor(data.gainLoss >= 0 ? .positiveChange : .negativeChange)
                
                Text("(\(data.gainLossPercent, specifier: "%.2f")%)")
                    .foregroundColor(data.gainLoss >= 0 ? .positiveChange : .negativeChange)
                
                Spacer()
            }
            .font(.subheadline)
        }
        .padding(Theme.cardPadding)
        .background(Color.cardBackground)
        .cornerRadius(Theme.cornerRadius)
        .shadow(radius: 2)
    }
}

struct PerformanceChartCard: View {
    let data: PortfolioData
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.itemSpacing) {
            Text("Performance")
                .font(.headline)
                .foregroundColor(.secondary)
            
            // Mock chart data
            Chart {
                ForEach(mockChartData, id: \.date) { point in
                    LineMark(
                        x: .value("Date", point.date),
                        y: .value("Value", point.value)
                    )
                    .foregroundStyle(.blue)
                }
            }
            .frame(height: 200)
        }
        .padding(Theme.cardPadding)
        .background(Color.cardBackground)
        .cornerRadius(Theme.cornerRadius)
        .shadow(radius: 2)
    }
}

struct TopHoldingsCard: View {
    let holdings: [UnifiedHolding]
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.itemSpacing) {
            Text("Top Holdings")
                .font(.headline)
                .foregroundColor(.secondary)
            
            ForEach(holdings.prefix(5), id: \.symbol) { holding in
                HoldingRowView(holding: holding)
            }
        }
        .padding(Theme.cardPadding)
        .background(Color.cardBackground)
        .cornerRadius(Theme.cornerRadius)
        .shadow(radius: 2)
    }
}

struct HoldingRowView: View {
    let holding: UnifiedHolding
    
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(holding.symbol)
                    .font(.headline)
                Text("\(holding.quantity, specifier: "%.2f") shares")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            VStack(alignment: .trailing) {
                Text("$\(holding.value, specifier: "%.2f")")
                    .font(.headline)
                Text("$\(holding.currentPrice, specifier: "%.2f")")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct NewsSentimentCard: View {
    @EnvironmentObject var container: DIContainer
    @State private var sentimentData: SentimentData?
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.itemSpacing) {
            Text("Market Sentiment")
                .font(.headline)
                .foregroundColor(.secondary)
            
            if let data = sentimentData {
                HStack {
                    Text("Overall Sentiment:")
                        .font(.subheadline)
                    
                    Spacer()
                    
                    Text(data.overallSentiment)
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(sentimentColor(data.overallScore))
                }
                
                ForEach(data.topHeadlines, id: \.title) { headline in
                    HStack {
                        Text(headline.title)
                            .font(.caption)
                            .lineLimit(2)
                        
                        Spacer()
                        
                        Text(headline.sentiment)
                            .font(.caption)
                            .foregroundColor(sentimentColor(headline.score))
                    }
                }
            } else {
                Text("Loading sentiment data...")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(Theme.cardPadding)
        .background(Color.cardBackground)
        .cornerRadius(Theme.cornerRadius)
        .shadow(radius: 2)
        .onAppear {
            loadSentimentData()
        }
    }
    
    private func loadSentimentData() {
        // Mock sentiment data
        sentimentData = SentimentData(
            overallScore: 0.3,
            overallSentiment: "Positive",
            topHeadlines: [
                SentimentHeadline(title: "Tech stocks rally on strong earnings", score: 0.7, sentiment: "Positive"),
                SentimentHeadline(title: "Market volatility concerns investors", score: -0.2, sentiment: "Neutral"),
                SentimentHeadline(title: "Fed signals potential rate cuts", score: 0.5, sentiment: "Positive")
            ]
        )
    }
    
    private func sentimentColor(_ score: Double) -> Color {
        if score > 0.3 {
            return .positiveChange
        } else if score < -0.3 {
            return .negativeChange
        } else {
            return .neutralChange
        }
    }
}

struct ErrorView: View {
    let message: String
    let retryAction: () -> Void
    
    var body: some View {
        VStack(spacing: Theme.itemSpacing) {
            Image(systemName: "exclamationmark.triangle")
                .font(.largeTitle)
                .foregroundColor(.warningOrange)
            
            Text("Error")
                .font(.headline)
            
            Text(message)
                .font(.caption)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            
            Button("Retry", action: retryAction)
                .buttonStyle(.borderedProminent)
        }
        .padding(Theme.cardPadding)
    }
}

// Mock data
private let mockChartData: [ChartDataPoint] = [
    ChartDataPoint(date: Date().addingTimeInterval(-86400 * 30), value: 95000),
    ChartDataPoint(date: Date().addingTimeInterval(-86400 * 25), value: 98000),
    ChartDataPoint(date: Date().addingTimeInterval(-86400 * 20), value: 102000),
    ChartDataPoint(date: Date().addingTimeInterval(-86400 * 15), value: 105000),
    ChartDataPoint(date: Date().addingTimeInterval(-86400 * 10), value: 103000),
    ChartDataPoint(date: Date().addingTimeInterval(-86400 * 5), value: 108000),
    ChartDataPoint(date: Date(), value: 110000)
]

struct ChartDataPoint {
    let date: Date
    let value: Double
}
