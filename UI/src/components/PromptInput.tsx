import type { ReactNode } from "react"

interface PromptInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  disabled?: boolean
  leftSlot?: ReactNode
}

export function PromptInput({ value, onChange, onSubmit, disabled = false, leftSlot }: PromptInputProps) {
  return (
    <div className="flex flex-col gap-3">
      <div className="rounded-2xl border border-slate-300 bg-white shadow-sm focus-within:border-brand-blue">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Describe your dream trip…"
          rows={6}
          className="w-full resize-none rounded-2xl bg-transparent p-4 text-base leading-relaxed text-slate-700 outline-none placeholder:text-slate-400"
        />
      </div>
      <div className="flex items-center justify-between gap-3">
        <div>{leftSlot}</div>
        <button
          type="button"
          onClick={onSubmit}
          disabled={disabled || value.trim().length === 0}
          className="rounded-xl bg-brand-blue px-5 py-2.5 text-sm font-semibold text-white shadow-md transition hover:opacity-90 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          Plan my trip
        </button>
      </div>
    </div>
  )
}
