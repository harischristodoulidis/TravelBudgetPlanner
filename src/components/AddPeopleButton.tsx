type AddPeopleButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

export function AddPeopleButton({ ...props }: AddPeopleButtonProps) {
  return (
    <button
      {...props}
      type="button"
      className="inline-flex items-center gap-2 rounded-full border border-brand-blue bg-white px-5 py-2 text-sm font-medium text-brand-blue shadow-sm transition cursor-pointer hover:bg-brand-blue-soft"
    >
      <span className="text-lg leading-none">+</span>
      Add people
    </button>
  );
}
