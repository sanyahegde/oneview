import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Login from './pages/Login'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import PortfolioDetail from './pages/PortfolioDetail'
import AmbientBackground from './components/AmbientBackground'
import './App.css'

function App() {
  return (
    <>
      <AmbientBackground />
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
          <Route path="/portfolio/:id" element={<Layout><PortfolioDetail /></Layout>} />
        </Routes>
      </Router>
    </>
  )
}

export default App

