import { useState, useEffect } from 'react'
import cryptoAPI from '../services/api'
import CryptoCard from './CryptoCard'
import ChartView from './ChartView'
import TechnicalIndicators from './TechnicalIndicators'
import CryptoSelector from './CryptoSelector'
import CUSTOM_TOKENS, { isCustomToken } from '../config/customTokens'
import './Dashboard.css'

function Dashboard() {
  const [selectedSymbol, setSelectedSymbol] = useState('DDD')
  const [selectedCoinId, setSelectedCoinId] = useState(null)
  const [topCryptos, setTopCryptos] = useState([])
  const [customTokens, setCustomTokens] = useState([])
  const [historicalData, setHistoricalData] = useState(null)
  const [indicators, setIndicators] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeframe, setTimeframe] = useState('30')

  useEffect(() => {
    loadAllCryptos()
  }, [])

  useEffect(() => {
    if (selectedSymbol) {
      loadCryptoData()
    }
  }, [selectedSymbol, timeframe])

  const loadAllCryptos = async () => {
    try {
      // Load top cryptocurrencies
      const topData = await cryptoAPI.getTopCryptocurrencies(8)

      // Load custom tokens
      const customTokensData = await Promise.all(
        CUSTOM_TOKENS.map(async (token) => {
          try {
            const data = await cryptoAPI.getTokenByContract(token.contractAddress, token.platform)
            return {
              ...data,
              isCustomToken: true,
              contractAddress: token.contractAddress
            }
          } catch (error) {
            console.error(`Error loading token ${token.symbol}:`, error)
            return null
          }
        })
      )

      const validCustomTokens = customTokensData.filter(t => t !== null)

      setTopCryptos(topData)
      setCustomTokens(validCustomTokens)
    } catch (error) {
      console.error('Error loading cryptos:', error)
    }
  }

  const loadCryptoData = async () => {
    setLoading(true)
    try {
      const isCustom = isCustomToken(selectedSymbol)

      if (isCustom) {
        // Find the custom token
        const customToken = customTokens.find(t => t.symbol === selectedSymbol)
        if (!customToken) {
          console.error('Custom token not found')
          setLoading(false)
          return
        }

        const coinId = customToken.coin_id
        setSelectedCoinId(coinId)

        // Load data using coin_id for custom tokens
        const [historical, technical] = await Promise.all([
          cryptoAPI.getTokenHistoricalData(coinId, parseInt(timeframe)),
          cryptoAPI.getTokenIndicators(coinId, parseInt(timeframe))
        ])

        setHistoricalData(historical)
        setIndicators(technical)
      } else {
        // Load data normally for standard cryptocurrencies
        setSelectedCoinId(null)
        const [historical, technical] = await Promise.all([
          cryptoAPI.getHistoricalData(selectedSymbol, parseInt(timeframe)),
          cryptoAPI.getTechnicalIndicators(selectedSymbol, parseInt(timeframe))
        ])

        setHistoricalData(historical)
        setIndicators(technical)
      }
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
            cryptos={[...customTokens, ...topCryptos]}
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
              {/* Custom Tokens First */}
              {customTokens.map((crypto) => (
                <CryptoCard
                  key={crypto.symbol}
                  crypto={crypto}
                  isSelected={crypto.symbol === selectedSymbol}
                  onClick={() => handleSymbolChange(crypto.symbol)}
                />
              ))}

              {/* Top Cryptocurrencies */}
              {topCryptos.slice(0, 4).map((crypto) => (
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
