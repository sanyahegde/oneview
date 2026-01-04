import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Holding {
  id: number;
  portfolio_id: number;
  symbol: string;
  quantity: number;
  average_cost: number;
  current_price: number | null;
  market_value: number | null;
  gain_loss: number | null;
  gain_loss_percent: number | null;
  created_at: string;
}

export interface Portfolio {
  id: number;
  user_id: number;
  name: string;
  holdings: Holding[];
  created_at: string;
  updated_at: string | null;
}

export interface PortfolioSummary {
  portfolio_id: number;
  portfolio_name: string;
  total_holdings: number;
  total_cost_basis: number;
  total_market_value: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  asset_allocation: Array<{
    symbol: string;
    allocation: number;
    value: number;
  }>;
  holdings: Holding[];
}

export interface NewsArticle {
  id: number;
  symbol: string;
  title: string;
  source: string | null;
  url: string | null;
  published_at: string;
  summary: string | null;
  sentiment_score: number | null;
}

export interface StockSentiment {
  symbol: string;
  sentiment_score: number;
  sentiment_label: string;
  news_count: number;
  calculated_at: string;
}

export interface PortfolioSnapshot {
  id: number;
  portfolio_id: number;
  total_value: number;
  total_cost_basis: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  snapshot_date: string;
}

export interface HistoricalPerformance {
  portfolio_id: number;
  portfolio_name: string;
  data_points: PortfolioSnapshot[];
  current_value: number;
  initial_value: number | null;
  total_return: number | null;
  total_return_percent: number | null;
}

export const portfolioApi = {
  getAll: async (): Promise<Portfolio[]> => {
    const response = await api.get('/portfolios/');
    return response.data;
  },

  getById: async (id: number): Promise<Portfolio> => {
    const response = await api.get(`/portfolios/${id}`);
    return response.data;
  },

  getSummary: async (id: number): Promise<PortfolioSummary> => {
    const response = await api.get(`/portfolios/${id}/summary`);
    return response.data;
  },

  create: async (name: string): Promise<Portfolio> => {
    const response = await api.post('/portfolios/', { name });
    return response.data;
  },

  addHolding: async (portfolioId: number, holding: {
    symbol: string;
    quantity: number;
    average_cost: number;
  }): Promise<Holding> => {
    const response = await api.post(`/portfolios/${portfolioId}/holdings`, holding);
    return response.data;
  },

  updateHolding: async (
    portfolioId: number,
    holdingId: number,
    updates: {
      quantity?: number;
      average_cost?: number;
      current_price?: number;
    }
  ): Promise<Holding> => {
    const response = await api.put(`/portfolios/${portfolioId}/holdings/${holdingId}`, updates);
    return response.data;
  },

  deleteHolding: async (portfolioId: number, holdingId: number): Promise<void> => {
    await api.delete(`/portfolios/${portfolioId}/holdings/${holdingId}`);
  },

  getPerformance: async (id: number, days: number = 30): Promise<HistoricalPerformance> => {
    const response = await api.get(`/portfolios/${id}/performance?days=${days}`);
    return response.data;
  },
};

export const newsApi = {
  getNewsForSymbol: async (symbol: string, limit: number = 10): Promise<NewsArticle[]> => {
    const response = await api.get(`/news/symbol/${symbol}?limit=${limit}`);
    return response.data;
  },

  getSentimentForSymbol: async (symbol: string): Promise<StockSentiment> => {
    const response = await api.get(`/news/sentiment/${symbol}`);
    return response.data;
  },

  getPortfolioSentiments: async (portfolioId: number): Promise<StockSentiment[]> => {
    const response = await api.get(`/news/portfolio/${portfolioId}/sentiments`);
    return response.data;
  },
};

export const chatbotApi = {
  getInsights: async (portfolioId: number): Promise<string> => {
    const response = await api.get(`/chatbot/portfolio/${portfolioId}/insights`);
    return response.data.response;
  },

  sendMessage: async (portfolioId: number, message: string): Promise<string> => {
    const response = await api.post(`/chatbot/portfolio/${portfolioId}/chat`, { message });
    return response.data.response;
  },
};

export default api;

