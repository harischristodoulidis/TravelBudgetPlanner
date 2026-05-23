import { Navigate, Route, Routes } from 'react-router-dom'
import { Header } from './components/Header'
import { TripDetailsScreen } from './screens/TripDetailsScreen'
import { PlanScreen } from './screens/PlanScreen'

export default function App() {
  return (
    <div className="flex min-h-full flex-col">
      <Header />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<PlanScreen />} />
          <Route path="/trip/:slug" element={<TripDetailsScreen />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  )
}
