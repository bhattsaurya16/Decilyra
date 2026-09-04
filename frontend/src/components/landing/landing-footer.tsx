import Link from "next/link";

import { BrandMark } from "@/components/brand-mark";

export function LandingFooter() {
  return (
    <footer className="border-t border-border py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 text-sm text-muted-foreground sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div className="flex items-center gap-2 text-foreground">
          <BrandMark className="h-5 w-5" />
          Decilyra
        </div>
        <p>From data to defensible decisions.</p>
        <div className="flex gap-4">
          <Link href="/dashboard" className="hover:text-foreground">
            App
          </Link>
          <a href="#security" className="hover:text-foreground">
            Governance
          </a>
        </div>
      </div>
    </footer>
  );
}
