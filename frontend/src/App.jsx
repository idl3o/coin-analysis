import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import Header from './components/Header'
import './App.css'

function App() {
  return (
    <div className="App">
      <Header />
      <Dashboard />
    </div>
  )
}

export default App
