import './Header.css'
import { TrendingUp } from 'lucide-react'

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <TrendingUp size={32} />
          <h1>Crypto Analysis Dashboard</h1>
        </div>
        <p className="subtitle">Real-time cryptocurrency technical analysis</p>
      </div>
    </header>
  )
}

export default Header
