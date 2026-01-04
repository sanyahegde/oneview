import { useEffect, useRef } from 'react'
import './AmbientBackground.css'

export default function AmbientBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const planetRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Animate planet
    if (planetRef.current) {
      const planet = planetRef.current
      let rotation = 0
      const animate = () => {
        rotation += 0.1
        planet.style.transform = `rotate(${rotation}deg)`
        requestAnimationFrame(animate)
      }
      animate()
    }

    // Floating tickers animation
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    const tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'AMZN', 'META', 'SPY']
    const particles: Array<{
      symbol: string
      x: number
      y: number
      speed: number
      opacity: number
    }> = []

    // Initialize particles
    for (let i = 0; i < 15; i++) {
      particles.push({
        symbol: tickers[Math.floor(Math.random() * tickers.length)],
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        speed: 0.1 + Math.random() * 0.2,
        opacity: 0.03 + Math.random() * 0.04
      })
    }

    let animationFrameId: number

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.fillStyle = '#ffffff'
      ctx.font = '300 14px Inter, sans-serif'
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
      animationFrameId = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      cancelAnimationFrame(animationFrameId)
    }
  }, [])

  return (
    <div className="ambient-background">
      <div className="ambient-planet" ref={planetRef}>
        <div className="planet-sphere"></div>
      </div>
      <canvas ref={canvasRef} className="ambient-tickers" />
    </div>
  )
}

