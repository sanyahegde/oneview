//  HTTPClient.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import Foundation
import Combine

class APIClient: ObservableObject {
    private let baseURL: String
    private let keychainStore: KeychainStore
    private let session: URLSession
    
    init(keychainStore: KeychainStore) {
        self.keychainStore = keychainStore
        self.baseURL = AppConfig.shared.apiBaseURL
        
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 60
        self.session = URLSession(configuration: config)
    }
    
    // MARK: - Authentication
    
    func login(email: String, password: String, completion: @escaping (Result<String, Error>) -> Void) {
        let endpoint = APIEndpoint.login(email: email, password: password)
        performRequest(endpoint) { (result: Result<TokenResponse, Error>) in
            switch result {
            case .success(let tokenResponse):
                completion(.success(tokenResponse.accessToken))
            case .failure(let error):
                completion(.failure(error))
            }
        }
    }
    
    func register(email: String, password: String, fullName: String, completion: @escaping (Result<Void, Error>) -> Void) {
        let endpoint = APIEndpoint.register(email: email, password: password, fullName: fullName)
        performRequest(endpoint) { (result: Result<User, Error>) in
            switch result {
            case .success:
                completion(.success(()))
            case .failure(let error):
                completion(.failure(error))
            }
        }
    }
    
    func getCurrentUser(completion: @escaping (Result<User, Error>) -> Void) {
        let endpoint = APIEndpoint.getCurrentUser
        performAuthenticatedRequest(endpoint, completion: completion)
    }
    
    // MARK: - Accounts
    
    func getAccounts(completion: @escaping (Result<[Account], Error>) -> Void) {
        let endpoint = APIEndpoint.getAccounts
        performAuthenticatedRequest(endpoint, completion: completion)
    }
    
    func linkAccount(provider: String, publicToken: String, completion: @escaping (Result<AccountLinkResponse, Error>) -> Void) {
        let endpoint = APIEndpoint.linkAccount(provider: provider, publicToken: publicToken)
        performAuthenticatedRequest(endpoint, completion: completion)
    }
    
    // MARK: - Holdings
    
    func getHoldings(completion: @escaping (Result<[UnifiedHolding], Error>) -> Void) {
        let endpoint = APIEndpoint.getHoldings
        performAuthenticatedRequest(endpoint, completion: completion)
    }
    
    // MARK: - Transactions
    
    func getTransactions(
        symbol: String? = nil,
        type: String? = nil,
        dateFrom: Date? = nil,
        dateTo: Date? = nil,
        page: Int = 1,
        pageSize: Int = 50,
        completion: @escaping (Result<PaginatedTransactions, Error>) -> Void
    ) {
        let endpoint = APIEndpoint.getTransactions(
            symbol: symbol,
            type: type,
            dateFrom: dateFrom,
            dateTo: dateTo,
            page: page,
            pageSize: pageSize
        )
        performAuthenticatedRequest(endpoint, completion: completion)
    }
    
    // MARK: - Portfolio
    
    func getPortfolioSummary(completion: @escaping (Result<PortfolioData, Error>) -> Void) {
        // Mock implementation for now
        let mockData = PortfolioData(
            totalValue: 125000.0,
            totalCost: 120000.0,
            gainLoss: 5000.0,
            gainLossPercent: 4.17,
            holdingsCount: 8,
            accountsCount: 3
        )
        completion(.success(mockData))
    }
    
    // MARK: - Private Methods
    
    private func performRequest<T: Codable>(_ endpoint: APIEndpoint, completion: @escaping (Result<T, Error>) -> Void) {
        guard let url = endpoint.url(baseURL: baseURL) else {
            completion(.failure(APIError.invalidURL))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let body = endpoint.body {
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: body)
            } catch {
                completion(.failure(error))
                return
            }
        }
        
        session.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse else {
                completion(.failure(APIError.invalidResponse))
                return
            }
            
            guard 200...299 ~= httpResponse.statusCode else {
                completion(.failure(APIError.httpError(httpResponse.statusCode)))
                return
            }
            
            guard let data = data else {
                completion(.failure(APIError.noData))
                return
            }
            
            do {
                let decoded = try JSONDecoder().decode(T.self, from: data)
                completion(.success(decoded))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
    
    private func performAuthenticatedRequest<T: Codable>(_ endpoint: APIEndpoint, completion: @escaping (Result<T, Error>) -> Void) {
        guard let token = keychainStore.getToken() else {
            completion(.failure(APIError.noToken))
            return
        }
        
        guard let url = endpoint.url(baseURL: baseURL) else {
            completion(.failure(APIError.invalidURL))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        if let body = endpoint.body {
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: body)
            } catch {
                completion(.failure(error))
                return
            }
        }
        
        session.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse else {
                completion(.failure(APIError.invalidResponse))
                return
            }
            
            guard 200...299 ~= httpResponse.statusCode else {
                completion(.failure(APIError.httpError(httpResponse.statusCode)))
                return
            }
            
            guard let data = data else {
                completion(.failure(APIError.noData))
                return
            }
            
            do {
                let decoded = try JSONDecoder().decode(T.self, from: data)
                completion(.success(decoded))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

// MARK: - API Errors

enum APIError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case noData
    case noToken
    case httpError(Int)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response"
        case .noData:
            return "No data received"
        case .noToken:
            return "No authentication token"
        case .httpError(let code):
            return "HTTP error: \(code)"
        }
    }
}
