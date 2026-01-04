import { useRef } from 'react'
import { Link } from 'react-router-dom'
import PlanetMap from '../components/PlanetMap'
import './Home.css'

export default function Home() {
  const planetContainerRef = useRef<HTMLDivElement>(null)

  return (
    <div className="home-page">
      <div className="home-content">
        {/* Spinning Planet */}
        <div className="home-planet-container" ref={planetContainerRef}>
          <PlanetMap />
        </div>
        
        {/* Main Title */}
        <h1 className="home-title">
          <span className="home-title-bold">One View</span>
        </h1>
        
        {/* Subtitle */}
        <p className="home-subtitle">
          Your unified portfolio dashboard
        </p>
        
        {/* CTA Buttons */}
        <div className="home-cta-buttons">
          <Link to="/login" className="home-cta-button primary">
            Sign In
          </Link>
          <Link to="/dashboard" className="home-cta-button">
            View Dashboard
          </Link>
        </div>
      </div>
    </div>
  )
}

