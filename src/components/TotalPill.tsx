interface TotalPillProps {
  total: string
}

export function TotalPill({ total }: TotalPillProps) {
  return (
    <div className="flex items-baseline justify-center gap-2">
      <span className="text-xs uppercase tracking-wide text-slate-500">Total</span>
      <span className="text-2xl font-bold text-slate-800">€ {total}</span>
      <span className="text-[10px] uppercase tracking-wide text-slate-400">per person</span>
    </div>
  )
}
