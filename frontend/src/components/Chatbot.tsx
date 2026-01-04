import { useState, useEffect, useRef } from 'react'
import { chatbotApi } from '../services/api'
import './Chatbot.css'

interface Message {
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatbotProps {
  portfolioId: number
}

export default function Chatbot({ portfolioId }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadInitialInsights()
  }, [portfolioId])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadInitialInsights = async () => {
    try {
      setIsLoading(true)
      const insights = await chatbotApi.getInsights(portfolioId)
      setMessages([{
        type: 'assistant',
        content: insights,
        timestamp: new Date()
      }])
    } catch (err) {
      console.error('Failed to load insights', err)
      setMessages([{
        type: 'assistant',
        content: 'Hi! I\'m your portfolio assistant. Ask me anything about your investments, or try "What stocks should I consider?" or "How is my portfolio performing?"',
        timestamp: new Date()
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    
    // Add user message
    const newUserMessage: Message = {
      type: 'user',
      content: userMessage,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newUserMessage])
    setIsLoading(true)

    try {
      const response = await chatbotApi.sendMessage(portfolioId, userMessage)
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: response,
        timestamp: new Date()
      }])
    } catch (err) {
      console.error('Chat error', err)
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: 'Sorry, I\'m having trouble right now. Please try again.',
        timestamp: new Date()
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const suggestedQuestions = [
    "How is my portfolio performing?",
    "What are my best performing stocks?",
    "Should I diversify more?",
    "What's my risk level?"
  ]

  if (isMinimized) {
    return (
      <div className="chatbot-minimized" onClick={() => setIsMinimized(false)}>
        <div className="chatbot-icon">💬</div>
        <span>AI Assistant</span>
        <div className="chatbot-notification">●</div>
      </div>
    )
  }

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="chatbot-header-content">
          <div className="chatbot-title">
            <span className="chatbot-icon-header">🤖</span>
            <span>AI Portfolio Assistant</span>
          </div>
          <button 
            className="chatbot-minimize-btn"
            onClick={() => setIsMinimized(true)}
          >
            −
          </button>
        </div>
      </div>

      <div className="chatbot-messages">
        {messages.length === 0 && !isLoading && (
          <div className="chatbot-welcome">
            <p>👋 Hi! I'm your AI portfolio assistant.</p>
            <p>I can help you analyze your investments, answer questions, and provide insights using real-time stock data.</p>
          </div>
        )}
        
        {messages.map((message, index) => (
          <div key={index} className={`chatbot-message chatbot-message-${message.type}`}>
            <div className="chatbot-message-content">
              {message.content}
            </div>
            <div className="chatbot-message-time">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="chatbot-message chatbot-message-assistant">
            <div className="chatbot-typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {messages.length > 0 && messages.length < 3 && (
          <div className="chatbot-suggestions">
            <p>Suggested questions:</p>
            {suggestedQuestions.slice(0, 2).map((question, idx) => (
              <button
                key={idx}
                className="chatbot-suggestion-btn"
                onClick={() => setInput(question)}
                disabled={isLoading}
              >
                {question}
              </button>
            ))}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="chatbot-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your portfolio..."
          disabled={isLoading}
          className="chatbot-input"
        />
        <button 
          type="submit" 
          disabled={!input.trim() || isLoading}
          className="chatbot-send-btn"
        >
          →
        </button>
      </form>
    </div>
  )
}

