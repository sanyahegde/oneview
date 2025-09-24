//  AppConfig.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import Foundation

struct AppConfig {
    static let shared = AppConfig()
    
    let baseURL: String
    let apiVersion: String
    let appGroupIdentifier: String
    
    private init() {
        #if DEBUG
        self.baseURL = "http://localhost:8000"
        #else
        self.baseURL = "https://api.portfolioai.com"
        #endif
        
        self.apiVersion = "v1"
        self.appGroupIdentifier = "group.com.portfolioai.app"
    }
    
    var apiBaseURL: String {
        return "\(baseURL)/api/\(apiVersion)"
    }
}
