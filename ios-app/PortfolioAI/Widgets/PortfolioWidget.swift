//  PortfolioWidget.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import WidgetKit
import SwiftUI

struct PortfolioWidget: Widget {
    let kind: String = "PortfolioWidget"
    
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: PortfolioProvider()) { entry in
            PortfolioWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("Portfolio Summary")
        .description("View your portfolio value and daily change.")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct PortfolioEntry: TimelineEntry {
    let date: Date
    let totalValue: Double
    let dailyChange: Double
    let dailyChangePercent: Double
}

struct PortfolioProvider: TimelineProvider {
    func placeholder(in context: Context) -> PortfolioEntry {
        PortfolioEntry(
            date: Date(),
            totalValue: 125000.0,
            dailyChange: 2500.0,
            dailyChangePercent: 2.0
        )
    }
    
    func getSnapshot(in context: Context, completion: @escaping (PortfolioEntry) -> ()) {
        let entry = PortfolioEntry(
            date: Date(),
            totalValue: 125000.0,
            dailyChange: 2500.0,
            dailyChangePercent: 2.0
        )
        completion(entry)
    }
    
    func getTimeline(in context: Context, completion: @escaping (Timeline<PortfolioEntry>) -> ()) {
        let currentDate = Date()
        let entry = PortfolioEntry(
            date: currentDate,
            totalValue: 125000.0,
            dailyChange: 2500.0,
            dailyChangePercent: 2.0
        )
        
        // Update every hour
        let nextUpdate = Calendar.current.date(byAdding: .hour, value: 1, to: currentDate)!
        let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))
        completion(timeline)
    }
}

struct PortfolioWidgetEntryView: View {
    var entry: PortfolioProvider.Entry
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: "chart.line.uptrend.xyaxis")
                    .foregroundColor(.blue)
                Text("Portfolio")
                    .font(.caption)
                    .foregroundColor(.secondary)
                Spacer()
            }
            
            Text("$\(entry.totalValue, specifier: "%.0f")")
                .font(.title2)
                .fontWeight(.bold)
            
            HStack {
                Image(systemName: entry.dailyChange >= 0 ? "arrow.up.right" : "arrow.down.right")
                    .foregroundColor(entry.dailyChange >= 0 ? .green : .red)
                    .font(.caption)
                
                Text("$\(abs(entry.dailyChange), specifier: "%.0f")")
                    .font(.caption)
                    .foregroundColor(entry.dailyChange >= 0 ? .green : .red)
                
                Text("(\(entry.dailyChangePercent, specifier: "%.1f")%)")
                    .font(.caption)
                    .foregroundColor(entry.dailyChange >= 0 ? .green : .red)
                
                Spacer()
            }
        }
        .padding()
        .background(Color(.systemBackground))
    }
}

@main
struct PortfolioWidgetBundle: WidgetBundle {
    var body: some Widget {
        PortfolioWidget()
    }
}
