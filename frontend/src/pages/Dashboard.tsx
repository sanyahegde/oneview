import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { portfolioApi, Portfolio } from '../services/api'
import './Dashboard.css'

export default function Dashboard() {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newPortfolioName, setNewPortfolioName] = useState('')

  useEffect(() => {
    loadPortfolios()
  }, [])

  const loadPortfolios = async () => {
    try {
      setLoading(true)
      const data = await portfolioApi.getAll()
      setPortfolios(data)
      setError(null)
    } catch (err) {
      setError('Failed to load portfolios')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePortfolio = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newPortfolioName.trim()) return

    try {
      setError(null)
      const portfolio = await portfolioApi.create(newPortfolioName.trim())
      console.log('Portfolio created successfully:', portfolio)
      setNewPortfolioName('')
      setShowCreateForm(false)
      await loadPortfolios()
    } catch (err: any) {
      console.error('Failed to create portfolio', err)
      const errorMessage = err?.response?.data?.detail || err?.message || 'Failed to create portfolio'
      setError(`Error: ${errorMessage}`)
      console.error('Full error:', err)
    }
  }

  if (loading) {
    return <div className="dashboard-loading">Loading portfolios...</div>
  }

  if (error && portfolios.length === 0) {
    return <div className="dashboard-error">{error}</div>
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Portfolio Dashboard</h2>
        <button 
          onClick={() => setShowCreateForm(!showCreateForm)} 
          className="create-portfolio-button"
        >
          {showCreateForm ? 'Cancel' : '+ Create Portfolio'}
        </button>
      </div>

      {showCreateForm && (
        <form onSubmit={handleCreatePortfolio} className="create-portfolio-form">
          <input
            type="text"
            placeholder="Portfolio name (e.g., My Investments)"
            value={newPortfolioName}
            onChange={(e) => setNewPortfolioName(e.target.value)}
            autoFocus
            required
          />
          <button type="submit">Create</button>
        </form>
      )}

      {error && portfolios.length > 0 && (
        <div className="dashboard-error-inline">{error}</div>
      )}

      {portfolios.length === 0 ? (
        <div className="empty-state">
          <h3>Welcome to One View!</h3>
          <p>Track your stock investments in one place.</p>
          <p>Create your first portfolio to get started.</p>
          {!showCreateForm && (
            <button 
              onClick={() => setShowCreateForm(true)}
              className="create-first-portfolio-button"
            >
              Create Your First Portfolio
            </button>
          )}
        </div>
      ) : (
        <div className="portfolios-grid">
          {portfolios.map((portfolio) => (
            <Link
              key={portfolio.id}
              to={`/portfolio/${portfolio.id}`}
              className="portfolio-card"
            >
              <h3>{portfolio.name}</h3>
              <p className="holdings-count">
                {portfolio.holdings.length} holding{portfolio.holdings.length !== 1 ? 's' : ''}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
