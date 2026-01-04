import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import PortfolioDetail from './pages/PortfolioDetail'
import AmbientBackground from './components/AmbientBackground'
import './App.css'

function App() {
  return (
    <>
      <AmbientBackground />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/portfolio/:id" element={<PortfolioDetail />} />
          </Routes>
        </Layout>
      </Router>
    </>
  )
}

export default App

