import Link from "next/link";

import { Button } from "@/components/ui/button";

export function LandingCta() {
  return (
    <section className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 className="max-w-xl text-3xl font-medium tracking-tight">Start with the foundation. Add truth later.</h2>
        <p className="mt-4 max-w-xl text-sm leading-6 text-muted-foreground">
          Phase 1 is the shell: workspace, API, and the surfaces the engine will fill. Open the app to inspect the
          routes.
        </p>
        <Button asChild className="mt-8">
          <Link href="/dashboard">Enter Decilyra</Link>
        </Button>
      </div>
    </section>
  );
}
