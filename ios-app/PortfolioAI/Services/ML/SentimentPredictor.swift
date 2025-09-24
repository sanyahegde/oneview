//  SentimentPredictor.swift
//  PortfolioAI
//
//  Created by PortfolioAI Team on 2024-01-01.
//

import Foundation
import CoreML

class SentimentPredictor: ObservableObject {
    private var model: MLModel?
    
    init() {
        loadModel()
    }
    
    private func loadModel() {
        // For now, we'll use a mock implementation
        // In production, this would load the actual Core ML model
        print("SentimentPredictor initialized (mock mode)")
    }
    
    func predict(text: String) -> Double {
        // Mock sentiment prediction
        // In production, this would use the Core ML model
        let mockScore = Double.random(in: -1.0...1.0)
        return mockScore
    }
    
    func predictSentiment(text: String) -> SentimentResult {
        let score = predict(text: text)
        
        let sentiment: String
        if score > 0.3 {
            sentiment = "Positive"
        } else if score < -0.3 {
            sentiment = "Negative"
        } else {
            sentiment = "Neutral"
        }
        
        return SentimentResult(score: score, sentiment: sentiment)
    }
    
    func analyzeHeadlines(_ headlines: [String]) -> [SentimentResult] {
        return headlines.map { predictSentiment(text: $0) }
    }
    
    func getOverallSentiment(from headlines: [String]) -> SentimentResult {
        let results = analyzeHeadlines(headlines)
        let averageScore = results.map { $0.score }.reduce(0, +) / Double(results.count)
        
        let sentiment: String
        if averageScore > 0.3 {
            sentiment = "Positive"
        } else if averageScore < -0.3 {
            sentiment = "Negative"
        } else {
            sentiment = "Neutral"
        }
        
        return SentimentResult(score: averageScore, sentiment: sentiment)
    }
}

struct SentimentResult {
    let score: Double
    let sentiment: String
}
