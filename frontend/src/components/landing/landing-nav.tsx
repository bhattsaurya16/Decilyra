import Link from "next/link";

import { BrandMark } from "@/components/brand-mark";
import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";

export function LandingNav() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/80 bg-background/75 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2.5">
          <BrandMark className="h-7 w-7" />
          <span className="text-sm font-medium tracking-tight">Decilyra</span>
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
          <a href="#how-it-works" className="transition-colors hover:text-foreground">
            How it works
          </a>
          <a href="#capabilities" className="transition-colors hover:text-foreground">
            Capabilities
          </a>
          <a href="#ask" className="transition-colors hover:text-foreground">
            Ask Decilyra
          </a>
          <a href="#security" className="transition-colors hover:text-foreground">
            Governance
          </a>
        </nav>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button asChild size="sm" variant="outline">
            <Link href="/dashboard">Open app</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
