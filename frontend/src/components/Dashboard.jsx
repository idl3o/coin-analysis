import { useState, useEffect } from 'react'
import cryptoAPI from '../services/api'
import CryptoCard from './CryptoCard'
import ChartView from './ChartView'
import TechnicalIndicators from './TechnicalIndicators'
import CryptoSelector from './CryptoSelector'
import './Dashboard.css'

function Dashboard() {
  const [selectedSymbol, setSelectedSymbol] = useState('BTC')
  const [topCryptos, setTopCryptos] = useState([])
  const [historicalData, setHistoricalData] = useState(null)
  const [indicators, setIndicators] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeframe, setTimeframe] = useState('30')

  useEffect(() => {
    loadTopCryptos()
  }, [])

  useEffect(() => {
    if (selectedSymbol) {
      loadCryptoData()
    }
  }, [selectedSymbol, timeframe])

  const loadTopCryptos = async () => {
    try {
      const data = await cryptoAPI.getTopCryptocurrencies(10)
      setTopCryptos(data)
    } catch (error) {
      console.error('Error loading top cryptos:', error)
    }
  }

  const loadCryptoData = async () => {
    setLoading(true)
    try {
      const [historical, technical] = await Promise.all([
        cryptoAPI.getHistoricalData(selectedSymbol, parseInt(timeframe)),
        cryptoAPI.getTechnicalIndicators(selectedSymbol, parseInt(timeframe))
      ])

      setHistoricalData(historical)
      setIndicators(technical)
    } catch (error) {
      console.error('Error loading crypto data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSymbolChange = (symbol) => {
    setSelectedSymbol(symbol)
  }

  const handleTimeframeChange = (days) => {
    setTimeframe(days)
  }

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <div className="top-section">
          <CryptoSelector
            cryptos={topCryptos}
            selectedSymbol={selectedSymbol}
            onSelectSymbol={handleSymbolChange}
          />
        </div>

        <div className="timeframe-selector">
          <button
            className={timeframe === '7' ? 'active' : ''}
            onClick={() => handleTimeframeChange('7')}
          >
            7D
          </button>
          <button
            className={timeframe === '30' ? 'active' : ''}
            onClick={() => handleTimeframeChange('30')}
          >
            30D
          </button>
          <button
            className={timeframe === '90' ? 'active' : ''}
            onClick={() => handleTimeframeChange('90')}
          >
            90D
          </button>
          <button
            className={timeframe === '180' ? 'active' : ''}
            onClick={() => handleTimeframeChange('180')}
          >
            180D
          </button>
        </div>

        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading analysis...</p>
          </div>
        ) : (
          <>
            <div className="main-content">
              <div className="chart-section">
                <ChartView
                  symbol={selectedSymbol}
                  historicalData={historicalData}
                  indicators={indicators}
                />
              </div>

              <div className="indicators-section">
                <TechnicalIndicators
                  symbol={selectedSymbol}
                  indicators={indicators}
                />
              </div>
            </div>

            <div className="crypto-grid">
              {topCryptos.slice(0, 6).map((crypto) => (
                <CryptoCard
                  key={crypto.symbol}
                  crypto={crypto}
                  isSelected={crypto.symbol === selectedSymbol}
                  onClick={() => handleSymbolChange(crypto.symbol)}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default Dashboard
