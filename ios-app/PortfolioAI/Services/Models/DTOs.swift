//  DTOs.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import Foundation

// MARK: - Authentication Models

struct User: Codable, Identifiable {
    let id: Int
    let email: String
    let fullName: String?
    let isActive: Bool
    let createdAt: String
    let updatedAt: String?
    
    enum CodingKeys: String, CodingKey {
        case id, email
        case fullName = "full_name"
        case isActive = "is_active"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

struct TokenResponse: Codable {
    let accessToken: String
    let tokenType: String
    
    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case tokenType = "token_type"
    }
}

// MARK: - Account Models

struct Account: Codable, Identifiable {
    let id: Int
    let userId: Int
    let provider: String
    let providerAccountId: String
    let accountType: String
    let name: String?
    let accessToken: String?
    let lastSync: String?
    let createdAt: String
    let updatedAt: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case provider
        case providerAccountId = "provider_account_id"
        case accountType = "account_type"
        case name
        case accessToken = "access_token"
        case lastSync = "last_sync"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

struct AccountLinkResponse: Codable {
    let accountId: Int
    let provider: String
    let status: String
    
    enum CodingKeys: String, CodingKey {
        case accountId = "account_id"
        case provider, status
    }
}

// MARK: - Holding Models

struct UnifiedHolding: Codable, Identifiable {
    let symbol: String
    let quantity: Double
    let avgCost: Double
    let currentPrice: Double
    let value: Double
    let accountId: Int
    let accountName: String?
    let provider: String?
    
    var id: String { symbol }
    
    var gainLoss: Double {
        value - (quantity * avgCost)
    }
    
    var gainLossPercent: Double {
        let cost = quantity * avgCost
        return cost > 0 ? (gainLoss / cost) * 100 : 0
    }
    
    enum CodingKeys: String, CodingKey {
        case symbol, quantity, value
        case avgCost = "avg_cost"
        case currentPrice = "current_price"
        case accountId = "account_id"
        case accountName = "account_name"
        case provider
    }
}

// MARK: - Transaction Models

struct Transaction: Codable, Identifiable {
    let id: Int
    let accountId: Int
    let symbol: String?
    let type: String
    let quantity: Double?
    let price: Double?
    let amount: Double
    let date: String
    let description: String?
    let createdAt: String
    
    enum CodingKeys: String, CodingKey {
        case id
        case accountId = "account_id"
        case symbol, type, quantity, price, amount, date, description
        case createdAt = "created_at"
    }
}

struct PaginatedTransactions: Codable {
    let items: [Transaction]
    let total: Int
    let page: Int
    let pageSize: Int
    let pages: Int
    
    enum CodingKeys: String, CodingKey {
        case items, total, page
        case pageSize = "page_size"
        case pages
    }
}

// MARK: - Portfolio Models

struct PortfolioData: Codable {
    let totalValue: Double
    let totalCost: Double
    let gainLoss: Double
    let gainLossPercent: Double
    let holdingsCount: Int
    let accountsCount: Int
    
    enum CodingKeys: String, CodingKey {
        case totalValue = "total_value"
        case totalCost = "total_cost"
        case gainLoss = "gain_loss"
        case gainLossPercent = "gain_loss_percent"
        case holdingsCount = "holdings_count"
        case accountsCount = "accounts_count"
    }
}

// MARK: - Sentiment Models

struct SentimentData: Codable {
    let overallScore: Double
    let overallSentiment: String
    let topHeadlines: [SentimentHeadline]
    
    enum CodingKeys: String, CodingKey {
        case overallScore = "overall_score"
        case overallSentiment = "overall_sentiment"
        case topHeadlines = "top_headlines"
    }
}

struct SentimentHeadline: Codable {
    let title: String
    let score: Double
    let sentiment: String
}

// MARK: - Error Models

struct APIErrorResponse: Codable {
    let detail: String
}
