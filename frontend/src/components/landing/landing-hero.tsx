import Link from "next/link";

import { Button } from "@/components/ui/button";

export function LandingHero() {
  return (
    <section className="mx-auto max-w-6xl px-4 pb-20 pt-16 sm:px-6 sm:pt-24">
      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">From data to defensible decisions.</p>
      <h1 className="mt-4 max-w-3xl text-4xl font-medium leading-[1.1] tracking-tight sm:text-5xl">
        Turn business data into decisions you can defend.
      </h1>
      <p className="mt-5 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
        Decilyra connects company data, determines which analytical methods are valid, runs deterministic analysis,
        and explains the result. AI is the interface — not the source of truth.
      </p>
      <div className="mt-8 flex flex-wrap gap-3">
        <Button asChild>
          <Link href="/dashboard">Explore the workspace</Link>
        </Button>
        <Button asChild variant="outline">
          <a href="#how-it-works">See the workflow</a>
        </Button>
      </div>
      <ProductPreview />
    </section>
  );
}

function ProductPreview() {
  return (
    <div className="mt-16 overflow-hidden rounded-lg border border-border bg-card shadow-[0_20px_50px_-32px_rgba(20,18,12,0.45)]">
      <div className="flex items-center justify-between border-b border-border px-4 py-2.5">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="h-2 w-2 rounded-full bg-border" />
          Illustrative product view · not live data
        </div>
        <span className="font-mono text-[11px] text-muted-foreground">workspace / overview</span>
      </div>
      <div className="grid gap-px bg-border md:grid-cols-[180px_minmax(0,1fr)]">
        <div className="hidden space-y-4 bg-sidebar p-4 md:block">
          {["Overview", "Data", "Analyze", "Findings", "Ask Decilyra"].map((item) => (
            <div key={item} className="text-xs text-muted-foreground">
              {item}
            </div>
          ))}
        </div>
        <div className="grid gap-3 bg-background p-4 sm:grid-cols-3">
          {[
            ["Revenue", "$4.82M"],
            ["Gross margin", "41.8%"],
            ["Customers", "12,480"],
          ].map(([label, value]) => (
            <div key={label} className="rounded-md border border-border bg-card p-3">
              <p className="text-[11px] uppercase tracking-[0.14em] text-muted-foreground">{label}</p>
              <p className="mt-2 font-mono text-xl">{value}</p>
            </div>
          ))}
          <div className="rounded-md border border-border bg-card p-3 sm:col-span-3">
            <p className="text-[11px] uppercase tracking-[0.14em] text-muted-foreground">Revenue trend</p>
            <svg viewBox="0 0 400 88" className="mt-4 h-20 w-full text-primary" aria-hidden="true">
              <path
                d="M0 62 C40 58, 70 70, 110 48 S180 20, 220 34 300 60, 400 18"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
