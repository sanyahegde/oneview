//  Endpoints.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import Foundation

enum APIEndpoint {
    // Authentication
    case login(email: String, password: String)
    case register(email: String, password: String, fullName: String)
    case getCurrentUser
    
    // Accounts
    case getAccounts
    case linkAccount(provider: String, publicToken: String)
    
    // Holdings
    case getHoldings
    
    // Transactions
    case getTransactions(symbol: String?, type: String?, dateFrom: Date?, dateTo: Date?, page: Int, pageSize: Int)
    
    var method: HTTPMethod {
        switch self {
        case .login, .register, .linkAccount:
            return .POST
        case .getCurrentUser, .getAccounts, .getHoldings, .getTransactions:
            return .GET
        }
    }
    
    var path: String {
        switch self {
        case .login:
            return "/auth/login"
        case .register:
            return "/auth/register"
        case .getCurrentUser:
            return "/auth/me"
        case .getAccounts:
            return "/accounts/"
        case .linkAccount:
            return "/accounts/link"
        case .getHoldings:
            return "/holdings/"
        case .getTransactions:
            return "/transactions/"
        }
    }
    
    var body: [String: Any]? {
        switch self {
        case .login(let email, let password):
            return ["email": email, "password": password]
        case .register(let email, let password, let fullName):
            return ["email": email, "password": password, "full_name": fullName]
        case .linkAccount(let provider, let publicToken):
            return ["provider": provider, "public_token": publicToken]
        default:
            return nil
        }
    }
    
    var queryItems: [URLQueryItem]? {
        switch self {
        case .getTransactions(let symbol, let type, let dateFrom, let dateTo, let page, let pageSize):
            var items: [URLQueryItem] = []
            
            if let symbol = symbol {
                items.append(URLQueryItem(name: "symbol", value: symbol))
            }
            if let type = type {
                items.append(URLQueryItem(name: "type", value: type))
            }
            if let dateFrom = dateFrom {
                items.append(URLQueryItem(name: "date_from", value: ISO8601DateFormatter().string(from: dateFrom)))
            }
            if let dateTo = dateTo {
                items.append(URLQueryItem(name: "date_to", value: ISO8601DateFormatter().string(from: dateTo)))
            }
            items.append(URLQueryItem(name: "page", value: String(page)))
            items.append(URLQueryItem(name: "page_size", value: String(pageSize)))
            
            return items.isEmpty ? nil : items
        default:
            return nil
        }
    }
    
    func url(baseURL: String) -> URL? {
        var components = URLComponents(string: baseURL + path)
        components?.queryItems = queryItems
        return components?.url
    }
}

enum HTTPMethod: String {
    case GET = "GET"
    case POST = "POST"
    case PUT = "PUT"
    case DELETE = "DELETE"
}
