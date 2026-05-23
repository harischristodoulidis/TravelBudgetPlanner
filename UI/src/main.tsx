import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { SessionProvider } from './context/SessionContext'
import { TripProvider } from './context/TripContext'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <SessionProvider>
        <TripProvider>
          <App />
        </TripProvider>
      </SessionProvider>
    </BrowserRouter>
  </StrictMode>,
)
