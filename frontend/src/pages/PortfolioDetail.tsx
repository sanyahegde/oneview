import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { portfolioApi, newsApi, PortfolioSummary, StockSentiment, HistoricalPerformance, NewsArticle } from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts'
import Chatbot from '../components/Chatbot'
import '../styles/charts.css'
import './PortfolioDetail.css'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']

export default function PortfolioDetail() {
  const { id } = useParams<{ id: string }>()
  const portfolioId = id ? parseInt(id) : null

  const [summary, setSummary] = useState<PortfolioSummary | null>(null)
  const [sentiments, setSentiments] = useState<StockSentiment[]>([])
  const [performance, setPerformance] = useState<HistoricalPerformance | null>(null)
  const [newsBySymbol, setNewsBySymbol] = useState<Record<string, NewsArticle[]>>({})
  const [expandedSymbol, setExpandedSymbol] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)
  const [newHolding, setNewHolding] = useState({
    symbol: '',
    quantity: '',
    average_cost: '',
  })

  useEffect(() => {
    if (portfolioId) {
      loadPortfolioData()
    }
  }, [portfolioId])

  const loadPortfolioData = async () => {
    if (!portfolioId) return

    try {
      setLoading(true)
      const [summaryData, sentimentsData, performanceData] = await Promise.all([
        portfolioApi.getSummary(portfolioId),
        newsApi.getPortfolioSentiments(portfolioId).catch(() => []),
        portfolioApi.getPerformance(portfolioId, 30).catch(() => null),
      ])
      setSummary(summaryData)
      setSentiments(sentimentsData)
      setPerformance(performanceData)
      setError(null)
    } catch (err) {
      setError('Failed to load portfolio data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const loadNewsForSymbol = async (symbol: string) => {
    if (newsBySymbol[symbol]) return // Already loaded
    
    try {
      const articles = await newsApi.getNewsForSymbol(symbol, 5)
      setNewsBySymbol(prev => ({ ...prev, [symbol]: articles }))
    } catch (err) {
      console.error(`Failed to load news for ${symbol}`, err)
    }
  }

  const handleAddHolding = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!portfolioId) return

    try {
      await portfolioApi.addHolding(portfolioId, {
        symbol: newHolding.symbol.toUpperCase(),
        quantity: parseFloat(newHolding.quantity),
        average_cost: parseFloat(newHolding.average_cost),
      })
      setNewHolding({ symbol: '', quantity: '', average_cost: '' })
      setShowAddForm(false)
      loadPortfolioData()
    } catch (err) {
      console.error('Failed to add holding', err)
    }
  }

  const handleDeleteHolding = async (holdingId: number) => {
    if (!portfolioId) return
    if (!confirm('Are you sure you want to delete this holding?')) return

    try {
      await portfolioApi.deleteHolding(portfolioId, holdingId)
      loadPortfolioData()
    } catch (err) {
      console.error('Failed to delete holding', err)
    }
  }

  const getSentimentForSymbol = (symbol: string): StockSentiment | undefined => {
    return sentiments.find(s => s.symbol === symbol)
  }

  const getSentimentColor = (label: string): string => {
    switch (label) {
      case 'positive':
        return '#10b981'
      case 'negative':
        return '#ef4444'
      default:
        return '#6b7280'
    }
  }

  const toggleNewsExpansion = (symbol: string) => {
    if (expandedSymbol === symbol) {
      setExpandedSymbol(null)
    } else {
      setExpandedSymbol(symbol)
      loadNewsForSymbol(symbol)
    }
  }

  // Format performance data for chart
  const performanceChartData = performance?.data_points.map(point => ({
    date: new Date(point.snapshot_date).toLocaleDateString(),
    value: point.total_value,
    gainLoss: point.total_gain_loss
  })) || []

  if (loading) {
    return <div className="portfolio-loading">Loading portfolio...</div>
  }

  if (error || !summary) {
    return (
      <div className="portfolio-error">
        {error || 'Portfolio not found'}
        <Link to="/">Back to Dashboard</Link>
      </div>
    )
  }

  return (
    <>
    <div className="portfolio-detail">
      <div className="portfolio-header">
        <Link to="/" className="back-link">← Back to Dashboard</Link>
        <h2>{summary.portfolio_name}</h2>
      </div>

      <div className="portfolio-stats">
        <div className="stat-card">
          <h3>Net Worth</h3>
          <p className="stat-value">${summary.total_market_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
        </div>
        <div className="stat-card">
          <h3>Total Gain/Loss</h3>
          <p className={`stat-value ${summary.total_gain_loss >= 0 ? 'positive' : 'negative'}`}>
            ${summary.total_gain_loss.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} 
            ({summary.total_gain_loss_percent.toFixed(2)}%)
          </p>
        </div>
        <div className="stat-card">
          <h3>Cost Basis</h3>
          <p className="stat-value">${summary.total_cost_basis.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
        </div>
        <div className="stat-card">
          <h3>Holdings</h3>
          <p className="stat-value">{summary.total_holdings}</p>
        </div>
      </div>

      <div className="portfolio-charts">
        <div className="chart-card">
          <h3>Historical Performance</h3>
          {performanceChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip 
                  formatter={(value: number) => `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#0088FE" 
                  strokeWidth={2}
                  name="Portfolio Value"
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="no-data-message">
              <p>No historical data available yet. Performance will be tracked over time.</p>
            </div>
          )}
          {performance && performance.total_return !== null && (
            <div className="performance-summary">
              <p>
                <strong>Total Return:</strong> {' '}
                <span className={performance.total_return >= 0 ? 'positive' : 'negative'}>
                  ${performance.total_return.toFixed(2)} ({performance.total_return_percent?.toFixed(2)}%)
                </span>
              </p>
            </div>
          )}
        </div>

        <div className="chart-card">
          <h3>Asset Allocation</h3>
          {summary.asset_allocation.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={summary.asset_allocation}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ symbol, allocation }) => `${symbol}: ${allocation.toFixed(1)}%`}
                  outerRadius={80}
                  fill="rgba(255, 255, 255, 0.2)"
                  dataKey="value"
                  stroke="var(--bg-secondary)"
                  strokeWidth={2}
                >
                  {summary.asset_allocation.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="no-data-message">
              <p>No holdings to display</p>
            </div>
          )}
        </div>
      </div>

      <div className="portfolio-holdings">
        <div className="holdings-header">
          <h3>Holdings with News & Sentiment</h3>
          <button onClick={() => setShowAddForm(!showAddForm)} className="add-button">
            {showAddForm ? 'Cancel' : '+ Add Holding'}
          </button>
        </div>

        {showAddForm && (
          <form onSubmit={handleAddHolding} className="add-holding-form">
            <input
              type="text"
              placeholder="Symbol (e.g., AAPL)"
              value={newHolding.symbol}
              onChange={(e) => setNewHolding({ ...newHolding, symbol: e.target.value })}
              required
            />
            <input
              type="number"
              step="0.01"
              placeholder="Quantity"
              value={newHolding.quantity}
              onChange={(e) => setNewHolding({ ...newHolding, quantity: e.target.value })}
              required
            />
            <input
              type="number"
              step="0.01"
              placeholder="Average Cost"
              value={newHolding.average_cost}
              onChange={(e) => setNewHolding({ ...newHolding, average_cost: e.target.value })}
              required
            />
            <button type="submit">Add</button>
          </form>
        )}

        <div className="holdings-list">
          {summary.holdings.map((holding) => {
            const sentiment = getSentimentForSymbol(holding.symbol)
            const news = newsBySymbol[holding.symbol] || []
            const isExpanded = expandedSymbol === holding.symbol
            
            return (
              <div key={holding.id} className="holding-card">
                <div className="holding-header">
                  <div className="holding-info">
                    <h4>{holding.symbol}</h4>
                    <div className="holding-metrics">
                      <span>Qty: {holding.quantity.toFixed(2)}</span>
                      <span>Avg Cost: ${holding.average_cost.toFixed(2)}</span>
                      <span>Current: ${holding.current_price?.toFixed(2) || 'N/A'}</span>
                      <span className={holding.gain_loss && holding.gain_loss >= 0 ? 'positive' : 'negative'}>
                        {holding.gain_loss !== null && holding.gain_loss_percent !== null
                          ? `$${holding.gain_loss.toFixed(2)} (${holding.gain_loss_percent.toFixed(2)}%)`
                          : 'N/A'}
                      </span>
                    </div>
                  </div>
                  <div className="holding-actions">
                    {sentiment && (
                      <span 
                        className="sentiment-badge"
                        style={{ backgroundColor: getSentimentColor(sentiment.sentiment_label) }}
                      >
                        {sentiment.sentiment_label}
                      </span>
                    )}
                    <button 
                      onClick={() => toggleNewsExpansion(holding.symbol)}
                      className="news-toggle-button"
                    >
                      {isExpanded ? '▲ Hide News' : '▼ Show News'}
                    </button>
                    <button 
                      onClick={() => handleDeleteHolding(holding.id)}
                      className="delete-button"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                
                {isExpanded && (
                  <div className="news-section">
                    {news.length > 0 ? (
                      <div className="news-list">
                        {news.map((article) => (
                          <div key={article.id} className="news-item">
                            <div className="news-header">
                              <h5>{article.title}</h5>
                              {article.source && <span className="news-source">{article.source}</span>}
                            </div>
                            {article.summary && (
                              <p className="news-summary">{article.summary}</p>
                            )}
                            {article.sentiment_score !== null && (
                              <div className="news-sentiment">
                                Sentiment Score: {article.sentiment_score.toFixed(2)}
                              </div>
                            )}
                            {article.url && (
                              <a href={article.url} target="_blank" rel="noopener noreferrer" className="news-link">
                                Read More →
                              </a>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="loading-news">Loading news...</div>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
    {portfolioId && <Chatbot portfolioId={portfolioId} />}
    </>
  )
}
