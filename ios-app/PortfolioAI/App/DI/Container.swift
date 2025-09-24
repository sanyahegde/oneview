//  Container.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import Foundation
import Combine

class DIContainer: ObservableObject {
    let apiClient: APIClient
    let keychainStore: KeychainStore
    let sentimentPredictor: SentimentPredictor
    
    init() {
        self.keychainStore = KeychainStore()
        self.apiClient = APIClient(keychainStore: keychainStore)
        self.sentimentPredictor = SentimentPredictor()
    }
}

class AuthenticationManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    
    private let keychainStore = KeychainStore()
    private let apiClient: APIClient
    
    init() {
        self.apiClient = APIClient(keychainStore: keychainStore)
    }
    
    func checkAuthenticationStatus() {
        if let token = keychainStore.getToken() {
            // Verify token is still valid
            apiClient.getCurrentUser { [weak self] result in
                DispatchQueue.main.async {
                    switch result {
                    case .success(let user):
                        self?.currentUser = user
                        self?.isAuthenticated = true
                    case .failure:
                        self?.logout()
                    }
                }
            }
        }
    }
    
    func login(email: String, password: String, completion: @escaping (Result<Void, Error>) -> Void) {
        apiClient.login(email: email, password: password) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let token):
                    self?.keychainStore.saveToken(token)
                    self?.isAuthenticated = true
                    completion(.success(()))
                case .failure(let error):
                    completion(.failure(error))
                }
            }
        }
    }
    
    func register(email: String, password: String, fullName: String, completion: @escaping (Result<Void, Error>) -> Void) {
        apiClient.register(email: email, password: password, fullName: fullName) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    // Auto-login after registration
                    self?.login(email: email, password: password, completion: completion)
                case .failure(let error):
                    completion(.failure(error))
                }
            }
        }
    }
    
    func logout() {
        keychainStore.deleteToken()
        isAuthenticated = false
        currentUser = nil
    }
}
