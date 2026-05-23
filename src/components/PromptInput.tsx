interface PromptInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  disabled?: boolean
}

export function PromptInput({ value, onChange, onSubmit, disabled = false }: PromptInputProps) {
  return (
    <div className="relative rounded-2xl border border-slate-300 bg-white shadow-sm focus-within:border-brand-blue">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Describe your dream trip…"
        rows={6}
        className="w-full resize-none rounded-2xl bg-transparent p-4 pr-14 text-sm leading-relaxed text-slate-700 outline-none placeholder:text-slate-400"
      />
      <button
        type="button"
        onClick={onSubmit}
        disabled={disabled || value.trim().length === 0}
        aria-label="Send prompt"
        className="absolute bottom-3 right-3 flex h-9 w-9 items-center justify-center rounded-full bg-brand-blue text-white shadow-md transition hover:opacity-90 disabled:cursor-not-allowed disabled:bg-slate-300"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
          <path d="M2.5 17.5l15-7.5-15-7.5v6l10 1.5-10 1.5v6z" />
        </svg>
      </button>
    </div>
  )
}
