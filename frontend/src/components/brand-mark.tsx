import { cn } from "@/lib/utils";

export function BrandMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={cn("text-primary", className)} aria-hidden="true">
      <path
        d="M8 26c0-8 3.2-14 8-16.5C20.8 12 24 18 24 26"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
      <path
        d="M11.5 24.5c0-5.4 2.1-9.5 4.5-11.2 2.4 1.7 4.5 5.8 4.5 11.2"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinecap="round"
        opacity="0.7"
      />
      <path d="M7 26.5h18" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <circle cx="16" cy="8" r="1.6" fill="currentColor" />
    </svg>
  );
}
