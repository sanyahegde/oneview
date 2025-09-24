//  Color+Theme.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import SwiftUI

extension Color {
    static let primaryBlue = Color(red: 0.0, green: 0.48, blue: 1.0)
    static let secondaryBlue = Color(red: 0.0, green: 0.38, blue: 0.8)
    static let successGreen = Color(red: 0.2, green: 0.78, blue: 0.35)
    static let warningOrange = Color(red: 1.0, green: 0.58, blue: 0.0)
    static let errorRed = Color(red: 1.0, green: 0.23, blue: 0.19)
    
    static let cardBackground = Color(.systemBackground)
    static let secondaryBackground = Color(.secondarySystemBackground)
    static let groupedBackground = Color(.systemGroupedBackground)
    
    static let positiveChange = successGreen
    static let negativeChange = errorRed
    static let neutralChange = Color(.secondaryLabel)
}

struct Theme {
    static let cornerRadius: CGFloat = 12
    static let cardPadding: CGFloat = 16
    static let sectionSpacing: CGFloat = 20
    static let itemSpacing: CGFloat = 8
}
