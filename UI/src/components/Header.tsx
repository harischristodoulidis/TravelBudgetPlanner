import { Logo } from './Logo'

export function Header() {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-200/60 bg-white/70 backdrop-blur">
      <div className="flex flex-col gap-1 px-6 py-3">
        <div className="flex items-center gap-2">
          <Logo className="h-7 w-7" />
          <span className="text-base font-semibold tracking-tight text-slate-800">
            BudgetTrip Planner
          </span>
        </div>
        <p className="text-xs text-slate-500">
          Group trips matched to your budget and habits.
        </p>
      </div>
    </header>
  )
}
