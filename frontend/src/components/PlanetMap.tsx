import { useEffect, useRef } from 'react'
import './PlanetMap.css'

export default function PlanetMap() {
  const planetRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // PLANET ROTATION ANIMATION
    // Continuous rotation using requestAnimationFrame loop
    // Rotates 360 degrees every 45 seconds (very slow but observable)
    let planetAnimationFrameId: number | null = null
    if (planetRef.current) {
      const planet = planetRef.current
      let rotation = 0
      // Rotation speed: 360 degrees / 45 seconds = 8 degrees/second
      // At 60fps: 8/60 = 0.133 degrees per frame
      const rotationSpeed = 360 / (45 * 60) // 0.133 degrees per frame for 45 second full rotation
      
      const animatePlanet = () => {
        rotation += rotationSpeed
        // Keep rotation within 0-360 to prevent overflow (though not strictly necessary)
        if (rotation >= 360) {
          rotation -= 360
        }
        planet.style.transform = `rotate(${rotation}deg)`
        planetAnimationFrameId = requestAnimationFrame(animatePlanet)
      }
      animatePlanet()
    }

    return () => {
      if (planetAnimationFrameId !== null) {
        cancelAnimationFrame(planetAnimationFrameId)
      }
    }
  }, [])

  return (
    <div className="planet-map-container" ref={planetRef}>
      <svg
        className="planet-map"
        viewBox="0 0 1000 500"
        preserveAspectRatio="xMidYMid meet"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* World map with white continents - simplified but recognizable shapes */}
        
        {/* North America */}
        <path
          d="M 120 80 L 140 60 L 180 70 L 220 85 L 260 100 L 300 120 L 320 140 L 340 160 L 360 180 L 380 200 L 390 220 L 400 240 L 400 260 L 390 280 L 380 300 L 370 320 L 350 340 L 330 360 L 300 370 L 270 380 L 240 375 L 210 365 L 185 350 L 165 330 L 150 310 L 140 290 L 130 270 L 125 250 L 120 230 L 115 210 L 110 190 L 110 170 L 115 150 L 120 130 L 120 110 L 120 90 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* South America */}
        <path
          d="M 240 340 L 270 330 L 300 340 L 320 360 L 340 380 L 350 400 L 355 420 L 350 440 L 340 455 L 325 465 L 305 470 L 285 465 L 270 455 L 260 440 L 255 420 L 250 400 L 245 380 L 240 360 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* Europe */}
        <path
          d="M 470 140 L 490 130 L 510 135 L 525 150 L 530 170 L 525 190 L 515 205 L 500 210 L 485 205 L 475 190 L 470 170 L 475 155 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* Africa */}
        <path
          d="M 510 210 L 540 200 L 570 210 L 590 230 L 600 250 L 605 270 L 605 290 L 600 310 L 590 330 L 575 345 L 555 355 L 535 350 L 520 340 L 510 320 L 505 300 L 505 280 L 508 260 L 510 240 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* Asia - Large continent */}
        <path
          d="M 580 80 L 640 70 L 700 80 L 750 100 L 780 130 L 800 160 L 810 190 L 815 220 L 810 250 L 800 280 L 785 305 L 765 325 L 740 340 L 710 345 L 680 340 L 655 325 L 635 305 L 620 280 L 610 250 L 605 220 L 600 190 L 595 160 L 590 130 L 585 100 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* India (subcontinent) */}
        <path
          d="M 680 240 L 710 230 L 730 245 L 735 265 L 730 280 L 720 290 L 705 295 L 690 290 L 680 275 L 675 260 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* Australia */}
        <path
          d="M 750 320 L 780 315 L 800 330 L 810 350 L 810 370 L 800 385 L 785 390 L 770 385 L 760 370 L 755 355 L 750 340 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* Greenland */}
        <path
          d="M 380 20 L 420 15 L 450 25 L 460 45 L 455 65 L 440 75 L 420 78 L 400 75 L 385 65 L 380 50 L 378 35 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* Japan */}
        <path
          d="M 840 180 L 860 175 L 875 185 L 878 200 L 872 210 L 860 215 L 848 210 L 840 200 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* British Isles */}
        <path
          d="M 480 140 L 495 135 L 505 145 L 505 155 L 498 160 L 488 158 L 482 150 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
        
        {/* Madagascar */}
        <path
          d="M 620 340 L 640 335 L 650 345 L 650 360 L 640 370 L 625 372 L 615 365 L 612 355 Z"
          fill="rgba(255, 255, 255, 0.5)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="1.5"
        />
      </svg>
    </div>
  )
}
