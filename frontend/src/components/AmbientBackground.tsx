import { useEffect, useRef } from 'react'
import PlanetMap from './PlanetMap'
import './AmbientBackground.css'

export default function AmbientBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const planetContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Floating tickers animation
    const canvas = canvasRef.current
    if (!canvas) {
      return
    }

    const ctx = canvas.getContext('2d')
    if (!ctx) {
      return
    }

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    const tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'AMZN', 'META', 'SPY', 'NFLX', 'DIS', 'AMD', 'INTC', 'CRM', 'ADBE', 'PYPL']
    const particles: Array<{
      symbol: string
      x: number
      y: number
      speed: number
      opacity: number
    }> = []

    // Initialize particles - MORE VISIBLE
    for (let i = 0; i < 25; i++) {
      particles.push({
        symbol: tickers[Math.floor(Math.random() * tickers.length)],
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        speed: 0.15 + Math.random() * 0.25,
        opacity: 0.15 + Math.random() * 0.2 // Much more visible (was 0.03-0.07)
      })
    }

    let tickerAnimationFrameId: number

    const animateTickers = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.fillStyle = '#ffffff'
      ctx.font = '500 16px Inter, sans-serif' // Bolder and larger
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'

      particles.forEach(particle => {
        particle.y -= particle.speed
        if (particle.y < -20) {
          particle.y = canvas.height + 20
          particle.x = Math.random() * canvas.width
        }

        ctx.globalAlpha = particle.opacity
        ctx.fillText(particle.symbol, particle.x, particle.y)
      })

      ctx.globalAlpha = 1
      tickerAnimationFrameId = requestAnimationFrame(animateTickers)
    }

    animateTickers()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      cancelAnimationFrame(tickerAnimationFrameId)
    }
  }, [])

  return (
    <div className="ambient-background">
      <div className="ambient-planet" ref={planetContainerRef}>
        <PlanetMap />
      </div>
      <canvas ref={canvasRef} className="ambient-tickers" />
    </div>
  )
}

